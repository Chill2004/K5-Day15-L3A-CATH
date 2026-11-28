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

## 3. Render (tuỳ chọn)

`web_app.py` đọc `PORT` nên chạy được trên Render (Web Service, gói Free): Build Command `pip install -r requirements.txt`, Start Command `python web_app.py`, đặt `MODEL_PROVIDER`, `MODEL_NAME`, `API_KEY` ở mục **Environment**. Cùng lưu ý bảo mật như trên.
