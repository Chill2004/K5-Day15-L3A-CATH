# DEPLOY — giao diện web cho bản chạy thử E3

`web_app.py` (Gradio) là lớp vỏ web quanh `answer(text)` trong `codebase/agent.py`. Không đổi luồng, `guard` hay công cụ; `python run.py`, `run.py check`, `run.py eval` vẫn chạy như cũ (khung CLI vẫn chỉ cần thư viện chuẩn). Gradio chỉ cần cho giao diện web.

Giao diện là **demo chat 2 cột**:

- **Trái — CHAT HỖ TRỢ VÍ:** khung chat mở bằng lời chào lấy từ giao dịch giả trong `codebase/tools.py` (vd "Giao dịch 2.500.000 đ (mã TX-2026-0001) của bạn đang được tạm giữ…"). Bong bóng chat chỉ hiện `tra_loi` (không hiện JSON thô). Mỗi tin nhắn vẫn gọi `answer(text)` **một lần, phân loại riêng** (spec.md §4 — chưa xử lý hội thoại nhiều lượt); dòng ghi chú dưới khung chat nói rõ điều này và nhắc không nhập OTP / mật khẩu / thông tin thật. Có 4 nút ví dụ (Gấp thật = C02, Bị giục chuyển tiền = C01, Giả nhân viên = C12, Nghi chiếm TK = C03) và nút **Làm mới** (xoá chat về lời chào, đặt lại bộ đếm, xoá cột phải).
- **Phải — AI QUYẾT ĐỊNH GÌ (của tin nhắn mới nhất):** nhóm, hành động (sau guard), lý do (`ly_do` của model), guard can thiệp (`vi_pham`), công cụ đã gọi + trạng thái (`found`, `confirmed_hold`, `sent`…), bản nháp chờ duyệt (huy hiệu **CHỜ TƯ VẤN VIÊN DUYỆT (draft)** nếu `release_transaction` / `lock_wallet` bị chặn thành bản nháp), tóm tắt cho tư vấn viên, model · token vào/ra · thời gian. Mọi số đọc từ output và trace (`tracing.end()`), không bịa. Ở chế độ giả có băng cảnh báo. Mục gập **Lịch sử quyết định** liệt kê các lượt trong phiên.
- **Giới hạn mềm 15 tin nhắn / phiên trình duyệt** (đổi bằng biến `MAX_TURNS_PER_SESSION`) để bảo vệ hạn mức model khi Space để Public. Hết lượt thì báo và chờ bấm **Làm mới**. Đây là giới hạn mềm (tải lại trang là phiên mới), không thay cho việc để Space Private khi dùng key thật.
- **HF Spaces / ZeroGPU:** `web_app.py` thử `import spaces` và đặt `@spaces.GPU` lên hàm suy luận `run_inference` (hết cảnh báo "No @spaces.GPU function detected"); trên máy không cài `spaces` thì dùng decorator rỗng. Đối tượng `demo` nằm ở cấp module (hết cảnh báo "Launching demo not found in `__main__`").

## 1. Chạy trên máy

Cần Python 3.10+. Đứng ở thư mục gốc repo (thấy `run.py`, `web_app.py`).

```bash
python -m pip install -r requirements.txt
python web_app.py
```

Mở trình duyệt: <http://127.0.0.1:7860>. Dừng: `Ctrl+C`.

**Chế độ giả (không gọi model, không tốn token):** để trống `MODEL_PROVIDER` trong `.env`, hoặc ép bằng biến môi trường:

```bash
# Git Bash / macOS / Linux
MODEL_PROVIDER=fake python web_app.py
```
```powershell
# PowerShell
$env:MODEL_PROVIDER = "fake"; python web_app.py
```

Ở chế độ giả, model luôn trả nhãn cố định (`chua_ro`), giao diện báo "⚠️ Đang chạy chế độ giả". Dùng để kiểm giao diện, **không** dùng để đánh giá chất lượng.

**Model thật:** điền `.env` (chép từ `.env.example`, xem `docs/connect-model.md`):

```
MODEL_PROVIDER=gemini
MODEL_NAME=gemini-3.1-flash-lite
API_KEY=<key của nhóm>
```

Rồi chạy `python web_app.py` (nhớ bỏ `MODEL_PROVIDER=fake` nếu đã đặt trong terminal; biến môi trường được ưu tiên hơn `.env`). Dòng cuối kết quả hiện tên model và token vào/ra > 0 là đã gọi model thật. Mỗi lần bấm là một lần gọi model, có tốn lượt miễn phí.

Đổi cổng: đặt biến `PORT` (mặc định 7860). App luôn nghe `0.0.0.0`.

## 2. Đưa lên Hugging Face Spaces (miễn phí)

Space miễn phí dùng phần cứng **CPU basic**; app ngủ khi không ai dùng một thời gian, lần mở sau khởi động lại sau vài chục giây.

1. Tạo tài khoản ở <https://huggingface.co>, vào **New Space**: đặt tên, **SDK: Gradio**, **Hardware: CPU basic (free)** (hoặc **ZeroGPU** — `web_app.py` đã có `@spaces.GPU` nên chạy được cả hai). Chọn **Private** nếu dùng key thật (xem lưu ý bảo mật bên dưới).
2. Tạo access token: **Settings → Access Tokens → New token**, quyền **Write**. Token này dùng làm mật khẩu khi `git push`.
3. Clone Space về một thư mục **ngoài** repo này, chép đúng 3 thứ cần chạy — `web_app.py`, `requirements.txt`, `codebase/` (không chép `.env`, `eval/`, `evidence/`, `traces/`, `data/`, `__pycache__/`):

   ```bash
   git clone https://huggingface.co/spaces/<user>/<space-name> e3-space
   cp web_app.py requirements.txt e3-space/
   cp -r codebase e3-space/ && rm -rf e3-space/codebase/__pycache__
   ```

4. Sửa `e3-space/README.md` cho phần đầu (YAML) như sau — dòng `app_file` là bắt buộc, vì file chạy tên `web_app.py` chứ không phải `app.py`:

   ```yaml
   ---
   title: E3 Ho tro giao dich bi tam giu
   emoji: 🛡️
   colorFrom: blue
   colorTo: green
   sdk: gradio
   sdk_version: 6.32.0
   app_file: web_app.py
   pinned: false
   ---
   ```

   `sdk_version` là bản đã thử trên máy (gradio 6.32.0). Nếu Space báo không có bản này, đổi theo số trong README mẫu mà Hugging Face tạo sẵn.

5. Đẩy lên:

   ```bash
   cd e3-space
   git add . && git commit -m "Deploy E3 web UI" && git push
   ```

6. Đặt biến cho model thật: trong Space vào **Settings → Variables and secrets**:
   - **New secret** `API_KEY` = key của nhóm (secret: không ai xem lại được, không hiện trong log).
   - **New variable** (hoặc secret) `MODEL_PROVIDER` = `gemini`, `MODEL_NAME` = `gemini-3.1-flash-lite`.

   Space tự khởi động lại; biến được đưa vào môi trường và `codebase/ai.py` đọc qua `os.environ`. Không đặt gì thì app chạy chế độ giả.

7. Mở tab **App** của Space, bấm thử 4 ca mẫu. Xem log khi lỗi: tab **Logs**.

**Lưu ý bảo mật:** Space **Public** + `API_KEY` thật = ai có link cũng gọi model bằng key của nhóm (tốn hạn mức). Để Space **Private** khi demo bằng key thật, hoặc để Public ở chế độ giả. Không bao giờ commit `.env` hay dán key vào code.

## 3. Render — Web Service gói Free (không cần thẻ)

Render build thẳng từ repo GitHub này, không cần chép file ra thư mục riêng như HF. Đã kiểm trên máy (chế độ giả): app mở cổng sau ~4 giây, dùng ~155 MB RAM (gói Free có 512 MB), `GET /` trả 200.

**Hai file chỉ dành cho Render** (không ảnh hưởng `run.py`, eval hay HF Spaces):

| File | Vì sao |
|---|---|
| `requirements-render.txt` | Chỉ cài `gradio==6.32.0` (bản đã thử). Bỏ `spaces` (chỉ cho HF ZeroGPU) và `google-play-scraper` (chỉ cho script thu bằng chứng) → build nhanh, nhẹ hơn. `requirements.txt` giữ nguyên cho HF Spaces / chạy trên máy. |
| `render.yaml` | Blueprint tuỳ chọn, ghi sẵn đúng các thông số ở bước 2–3 dưới đây. Không chứa key. |

### Bước 1 — Kiểm repo trước khi đẩy

```bash
git status                       # không thấy .env trong danh sách
git check-ignore -v .env         # phải in ra: .gitignore:2:.env  .env
git ls-files | grep -i "\.env"   # chỉ được thấy .env.example
```

- `.env` (key thật) đã nằm trong `.gitignore` — Render **không** đọc `.env`; key đặt ở bước 3.
- `eval/run-N.csv`, `traces/run-N.jsonl`, `cost/simulate-N.csv` **phải commit** (là bài nộp, xem `.gitignore`). Chúng chỉ là dữ liệu giả, lên Render cũng không sao — app không đọc chúng. Các lượt nháp (`run-try`, `run-fake`…) đã được ignore sẵn.
- Không commit dữ liệu thật, `evidence/raw/`, `data-btc/` (đã ignore).
- Đẩy nhánh muốn deploy lên GitHub (repo Private cũng được — Render xin quyền đọc qua GitHub).

### Bước 2 — Tạo Web Service (Free)

1. Đăng ký <https://render.com> bằng tài khoản GitHub (gói Free không đòi thẻ).
2. **New → Web Service** → chọn repo này → chọn **Branch** cần chạy.
3. Điền:

   | Mục | Giá trị |
   |---|---|
   | Language / Runtime | `Python 3` |
   | Root Directory | để trống |
   | Build Command | `pip install -r requirements-render.txt` |
   | Start Command | `python web_app.py` |
   | Instance Type | **Free** |
   | Health Check Path (Advanced) | `/` |

   Không cần đặt `PORT`: Render tự cấp (mặc định 10000), `web_app.py` đọc `PORT` và nghe `0.0.0.0`.

   *Cách khác:* **New → Blueprint** → chọn repo → Render đọc `render.yaml` và tự điền như trên. Nếu Render đòi thông tin thanh toán ở luồng Blueprint, quay lại tạo bằng tay theo bảng trên.

### Bước 3 — Biến môi trường (mục **Environment**)

| Key | Giá trị | Ghi chú |
|---|---|---|
| `PYTHON_VERSION` | `3.13.7` | Bắt buộc nên có: service mới trên Render mặc định Python 3.14, còn app đã thử trên 3.13. |
| `MODEL_PROVIDER` | `fake` (thử) → `gemini` (demo thật) | Để `fake` = không gọi model, không tốn lượt. |
| `MODEL_NAME` | `gemini-3.1-flash-lite` | Cùng giá trị như `.env` trên máy. |
| `API_KEY` | key của nhóm | Chỉ nhập ở đây. Không dán vào code, `render.yaml`, slide, ảnh chụp màn hình. |
| `MAX_TURNS_PER_SESSION` | `15` | Tuỳ chọn, giới hạn mềm số tin / phiên. |
| `GRADIO_ANALYTICS_ENABLED` | `False` | Tuỳ chọn, tắt gửi thống kê của Gradio. |

Bấm **Save, rebuild and deploy** (đổi biến sau này cũng vậy — service tự khởi động lại).

### Bước 4 — Kiểm sau khi deploy

1. Tab **Logs**: build xong thấy `Running on local URL: http://0.0.0.0:10000`, trạng thái **Live**.
2. Mở `https://<tên-service>.onrender.com`, bấm 4 nút ví dụ.
3. Với `MODEL_PROVIDER=fake`: cột phải có băng "⚠️ Đang chạy chế độ giả". Với model thật: cột phải hiện tên model và token vào/ra > 0.
4. Lỗi gọi model (sai key, hết lượt): xem **Logs**; giao diện không bao giờ in API key.

### Lưu ý gói Free, bảo mật và hạn mức

- **Ngủ sau ~15 phút không có truy cập**; lần mở đầu tiên sau đó chờ khoảng 1 phút (cold start). Trước giờ demo, mở link sớm vài phút cho app thức.
- 750 giờ chạy Free / workspace / tháng — đủ cho 1 service chạy suốt tháng. Ổ đĩa không lưu lâu dài (mỗi lần deploy/ngủ dậy là mới), nhưng app web không ghi file nên không ảnh hưởng.
- **Link `onrender.com` là công khai** (gói Free không có chế độ Private như HF Space). Ai có link + `API_KEY` thật = gọi model bằng hạn mức của nhóm. Vì vậy:
  - Mặc định để `MODEL_PROVIDER=fake`; chỉ đổi sang `gemini` quanh giờ demo, xong đổi lại `fake` (hoặc **Suspend** service).
  - Dùng key riêng cho demo, đặt giới hạn / hạn mức thấp ở phía nhà cung cấp; lộ thì thu hồi key ngay.
  - `MAX_TURNS_PER_SESSION` chỉ là giới hạn mềm (tải lại trang là phiên mới), không thay cho các biện pháp trên.
  - Không gửi link công khai lên nhóm chat lớn khi đang bật key thật.
- App xử lý từng lượt một (`queue(default_concurrency_limit=1)` + khoá) — nhiều người bấm cùng lúc thì xếp hàng, không lỗi.
