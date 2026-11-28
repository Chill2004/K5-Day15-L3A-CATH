# DEPLOY — giao diện web cho bản chạy thử E3

`web_app.py` (Gradio) là lớp vỏ web quanh `answer(text)` trong `codebase/agent.py`. Không đổi luồng, `guard` hay công cụ; `python run.py`, `run.py check`, `run.py eval` vẫn chạy như cũ (khung CLI vẫn chỉ cần thư viện chuẩn). Gradio chỉ cần cho giao diện web.

Giao diện hiện `nhom`, `hanh_dong` (sau guard), `tra_loi`, `tom_tat`, bảng trạng thái công cụ lấy từ trace (`sent`, `confirmed_hold`, `found`…) và luật cứng: `release_transaction` / `lock_wallet` chỉ tạo `draft` chờ người duyệt. Có 4 nút ca mẫu: C02, C12, C01, C03.

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

1. Tạo tài khoản ở <https://huggingface.co>, vào **New Space**: đặt tên, **SDK: Gradio**, **Hardware: CPU basic (free)**. Chọn **Private** nếu dùng key thật (xem lưu ý bảo mật bên dưới).
2. Tạo access token: **Settings → Access Tokens → New token**, quyền **Write**. Token này dùng làm mật khẩu khi `git push`.
3. Clone Space về một thư mục **ngoài** repo này, chép đúng 3 thứ cần chạy (không chép `.env`, `eval/`, `evidence/`, `traces/`):

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

## 3. Render (tuỳ chọn)

`web_app.py` đọc `PORT` nên chạy được trên Render (Web Service, gói Free): Build Command `pip install -r requirements.txt`, Start Command `python web_app.py`, đặt `MODEL_PROVIDER`, `MODEL_NAME`, `API_KEY` ở mục **Environment**. Cùng lưu ý bảo mật như trên.
