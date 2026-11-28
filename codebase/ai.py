"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import re
import time
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


SHOW_RAW = False   # đổi thành True để in nguyên phản hồi của API khi cần tìm tên trường


RETRY_CODES = (429, 500, 503)   # quá lượt / model quá tải: lỗi tạm thời, thử lại
RETRY_WAITS = (2, 5, 10, 20)    # giây chờ trước mỗi lần thử lại


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib).
    Lỗi tạm thời (429, 500, 503) thì chờ rồi thử lại tối đa len(RETRY_WAITS) lần."""
    payload = json.dumps(body).encode("utf-8")
    for attempt in range(len(RETRY_WAITS) + 1):
        req = urllib.request.Request(
            url, data=payload, method="POST",
            headers=dict({"Content-Type": "application/json"}, **headers))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code in RETRY_CODES and attempt < len(RETRY_WAITS):
                time.sleep(RETRY_WAITS[attempt])
                continue
            raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
        except (TimeoutError, urllib.error.URLError, ConnectionError) as e:
            # mạng chậm / hết thời gian chờ: cũng là lỗi tạm thời, thử lại
            if attempt < len(RETRY_WAITS):
                time.sleep(RETRY_WAITS[attempt])
                continue
            raise RuntimeError("Lỗi mạng sau %d lần thử: %s" % (attempt + 1, e))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


@model_call
def call_model(system: str, user: str, schema: dict = None) -> dict:
    """schema (tuỳ chọn): JSON schema kiểu Gemini — có thì model bắt buộc trả JSON đúng schema,
    "text" là chuỗi JSON. Không có thì trả chữ thường như cũ."""
    if MODEL_PROVIDER == "fake":
        if schema:  # chế độ giả: trả JSON hợp lệ theo schema để luồng phía sau vẫn chạy được
            fake = {k: (v.get("enum") or ["[giả]"])[-1] for k, v in schema.get("properties", {}).items()}
            return {"text": json.dumps(fake, ensure_ascii=False), "model": "fake", "tokens_in": 0, "tokens_out": 0}
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER == "gemini":
        r = call_gemini(system, user, schema)
    elif MODEL_PROVIDER == "openrouter":
        r = call_openrouter(system, user, schema)
    else:
        raise NotImplementedError(
            "chưa viết phần gọi model cho MODEL_PROVIDER=%s — hỗ trợ: fake, gemini, openrouter; xem docs/connect-model.md"
            % MODEL_PROVIDER)
    return {"text": r["text"], "model": r.get("model") or MODEL_NAME,
            "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}


URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent"


def call_gemini(system, user, schema=None):
    """Gọi Gemini qua REST API (generateContent). Key gửi ở header, không nằm trong URL."""
    body = {"contents": [{"role": "user", "parts": [{"text": user}]}]}
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    if schema:
        body["generationConfig"] = {"responseMimeType": "application/json", "responseSchema": schema}
    data = post_json(URL_GEMINI % MODEL_NAME, {"x-goog-api-key": API_KEY}, body)
    cands = data.get("candidates") or []
    parts = (cands[0].get("content") or {}).get("parts", []) if cands else []
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    u = data.get("usageMetadata", {})
    # Token ra = token trả lời + token suy nghĩ (model "thinking" tính tiền cả phần suy nghĩ).
    tokens_out = u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)
    return {"text": text, "tokens_in": u.get("promptTokenCount", 0), "tokens_out": tokens_out}


URL_OPENROUTER = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_DEFAULT_MODEL = "deepseek/deepseek-v4.1-flash-1017"
OPENROUTER_HEADERS = {
    "HTTP-Referer": "https://k5-day15-l3a-cath.onrender.com",
    "X-Title": "E3 Wallet Guard",
}


def _to_json_schema(s):
    """Đổi schema kiểu Gemini (type viết HOA, propertyOrdering) sang JSON Schema chuẩn cho OpenAI / OpenRouter."""
    if not isinstance(s, dict):
        return s
    out = {}
    for k, v in s.items():
        if k == "propertyOrdering":
            continue
        if k == "type" and isinstance(v, str):
            out[k] = v.lower()
        elif k == "properties":
            out[k] = {name: _to_json_schema(sub) for name, sub in v.items()}
        elif k == "items":
            out[k] = _to_json_schema(v)
        else:
            out[k] = v
    if out.get("type") == "object":
        out.setdefault("additionalProperties", False)  # strict mode của json_schema đòi trường này
    return out


_FENCE = re.compile(r"^\s*```[a-zA-Z0-9_-]*\s*\n?(.*?)\n?\s*```\s*$", re.DOTALL)


def _strip_fences(text):
    """Bỏ khung ```json ... ``` nếu model bọc JSON trong Markdown; còn chữ thừa quanh JSON thì lấy { … } ngoài cùng."""
    t = (text or "").strip()
    m = _FENCE.match(t)
    if m:
        t = m.group(1).strip()
    if not t.startswith("{"):
        a, b = t.find("{"), t.rfind("}")
        if a != -1 and b > a:
            t = t[a:b + 1]
    return t


def call_openrouter(system, user, schema=None):
    """Gọi OpenRouter (API kiểu OpenAI chat/completions) bằng urllib. Key gửi ở header Authorization.
    Token lấy từ usage.prompt_tokens / usage.completion_tokens (completion đã gồm token suy luận)."""
    key = API_KEY or (os.environ.get("OPENROUTER_API_KEY") or "").strip()
    if not key:
        raise RuntimeError("MODEL_PROVIDER=openrouter nhưng chưa có API_KEY (hoặc OPENROUTER_API_KEY) "
                           "trong biến môi trường / .env")
    model = MODEL_NAME or OPENROUTER_DEFAULT_MODEL
    messages = []
    if system or schema:
        sys_text = system or ""
        if schema:
            # Nhắc thêm bằng lời: không phải model / nhà cung cấp nào trên OpenRouter cũng tôn trọng response_format.
            sys_text += ("\n\n## Định dạng trả lời\nChỉ trả về MỘT object JSON hợp lệ, không bọc ```, không thêm chữ "
                         "ngoài JSON, đúng các khoá: %s." % ", ".join(schema.get("properties", {})))
        messages.append({"role": "system", "content": sys_text})
    messages.append({"role": "user", "content": user})
    body = {"model": model, "messages": messages}
    if schema:
        body["response_format"] = {"type": "json_schema", "json_schema": {
            "name": "tra_loi", "strict": True, "schema": _to_json_schema(schema)}}
    headers = dict(OPENROUTER_HEADERS, Authorization="Bearer " + key)
    data = post_json(URL_OPENROUTER, headers, body)
    if data.get("error"):
        err = data["error"]
        raise RuntimeError("OpenRouter lỗi: %s" % (err.get("message") if isinstance(err, dict) else err))
    choices = data.get("choices") or []
    content = ((choices[0].get("message") or {}).get("content") if choices else "") or ""
    if isinstance(content, list):  # một số model trả content dạng danh sách phần
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
    text = _strip_fences(content) if schema else content
    u = data.get("usage") or {}
    return {"text": text, "model": model,
            "tokens_in": u.get("prompt_tokens", 0), "tokens_out": u.get("completion_tokens", 0)}
