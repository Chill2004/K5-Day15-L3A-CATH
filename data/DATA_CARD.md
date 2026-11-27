# DATA CARD: Giao dịch bị giữ & Tin nhắn hỗ trợ (Synthetic)

## 1. Tổng quan
- **Nguồn dữ liệu:** Dữ liệu giả lập (`synthetic`), 30 dòng đầu sinh bằng gen_synthetic.py seed 42; 10 dòng sau (TX0031–TX0040, M0031–M0040) Hà viết tay thêm.
- **Mục đích:** Đóng vai trò môi trường giả lập (benchmark / offline eval) cho hệ thống Agent hỗ trợ phân loại và xử lý các giao dịch nghi ngờ / bị tạm giữ.
- **Quy mô:**
  - `held_transactions.csv`: 40 giao dịch bị giữ.
  - `messages.csv`: 40 tin nhắn phản hồi từ người dùng tương ứng.

## 2. Cấu trúc trường dữ liệu
### `held_transactions.csv`
- `tx_id`: Mã định danh giao dịch (`TX0001` - `TX0040`).
- `user_id`: Mã người dùng (`Uxxx`).
- `thoi_gian`: Thời điểm thực hiện giao dịch (YYYY-MM-DD HH:MM).
- `so_tien_vnd`: Số tiền giao dịch (VND).
- `kenh`: Kênh giao dịch (`chuyen_vi`, `thanh_toan_qr`, `chuyen_ngan_hang`).
- `loai_nguoi_nhan`: Phân loại bên nhận (`ngan_hang`, `ca_nhan`, `cua_hang`, `vi_khac`).
- `nguoi_nhan_da_chuyen_truoc`: Đã từng giao dịch trước đó chưa (`co` / `khong`).
- `thiet_bi_moi`: Thực hiện từ thiết bị mới hay không (`co` / `khong`).
- `ly_do_giu`: Lý do hệ thống tạm giữ (`thiet_bi_moi`, `nguoi_nhan_moi`, `gio_bat_thuong`, `so_tien_bat_thuong`, `nguoi_nhan_bi_bao_cao`).
- `trang_thai`: Trạng thái xử lý (`dang_giu`).
- `nhom_that`: Nhãn ground-truth (`bi_giuc`, `gap_that`, `chiem_tk`, `chua_ro`).
- `nhan`: `synthetic`.

### `messages.csv`
- `msg_id`: Mã tin nhắn (`M0001` - `M0040`).
- `tx_id`: Mã giao dịch tương ứng.
- `tin_nhan`: Nội dung tin nhắn người dùng gửi lên hỗ trợ (đã được tinh chỉnh tự nhiên, hoảng loạn, không lặp câu).
- `nhom_that`: Nhãn ground-truth tương ứng.
- `ngoai_gio`: Ngoài giờ hành chính hay không (`co` / `khong`).
- `nguon`: `tu_viet`.
- `nhan`: `synthetic`.

## 3. Phân bố 4 nhóm
- `bi_giuc` (12/40 - 30%): Người dùng bị thao túng tâm lý, giục giã chuyển tiền gấp (giả công an, viện phí tai nạn, sàn đầu tư, làm nhiệm vụ Telegram, cọc hàng gấp, nhân viên ngân hàng giả).
- `gap_that` (11/40 - 27.5%): Nhu cầu thanh toán thực tế, cấp bách (học phí con đến hạn, tiền trọ chủ nhà đứng đòi, tiền hàng nông sản/hải sản xe sắp chạy, khách đợi lấy hàng).
- `chiem_tk` (9/40 - 22.5%): Dấu hiệu tài khoản bị xâm phạm (thiết bị lạ đăng nhập, bị hack SIM đổi mật khẩu ví, vừa mất máy điện thoại, phát sinh lệnh chuyển tiền khi đang ngủ).
- `chua_ro` (8/40 - 20%): Tin nhắn cộc lốc, hỏi chung chung, từ ngữ tối giản hoặc chỉ có ký tự đặt câu hỏi.

## 4. Kiểm định chất lượng dữ liệu & Phân tích các ca biên (Edge Cases)
- **Người thực hiện kiểm tay:** Nguyễn Thị Thu Hà
- **Số dòng kiểm tra:** 40/40 dòng.
- **Kết quả nghiệm thu:** 40/40 dòng đạt tiêu chí phân loại, văn phong thực tế, giàu cảm xúc hoảng loạn và phản ánh chân thực các tình huống giao dịch tại Việt Nam.

###  Ghi chú đặc biệt về các ca biên & mơ hồ cố ý (Tránh tranh cãi khi chấm Eval):
1. **Ca khó giữa `bi_giuc` và `gap_that` (Mơ hồ cố ý - Intentional Ambiguity):**
   - **`M0026` (Tin báo con tai nạn cấp cứu mổ gấp) & `M0025` (Shop giục cọc giữ đồ sale 15 phút):** 
     - *Phân loại:* Gắn nhãn `bi_giuc`.
     - *Lý do:* Về bản chất thực tế, đây là hai chiêu thức lừa đảo thao túng tâm lý điển hình (tạo áp lực thời gian cực đoan, khai thác lòng trắc ẩn hoặc tâm lý sợ bỏ lỡ FOMO).
     - *Lưu ý khi đánh giá:* Tâm lý người dùng lúc nhắn tin tin rằng họ đang **gấp thật**. Mô hình AI cần kết hợp ngữ cảnh tin nhắn với tín hiệu bất thường trong giao dịch (ví dụ: `nguoi_nhan_bi_bao_cao` ở TX0026, `thiet_bi_moi` ở TX0025) để nhận diện bẫy thao túng thay vì chỉ tin vào lời trần tình của người dùng.
2. **Ca `gap_that` có rủi ro bị kẻ gian lợi dụng kịch bản quen thuộc:**
   - **`M0015` (Chủ trọ đứng réo trước cửa) & `M0003` (Học phí trước 17h khóa cổng):**
     - *Phân loại:* Gắn nhãn `gap_that`.
     - *Lý do:* Phản ánh các nghĩa vụ thanh toán định kỳ, quen thuộc trong đời sống.
     - *Lưu ý khi đánh giá:* Không xem nhãn này là "đúng tuyệt đối 100% độc lập". Kẻ gian hoàn toàn có thể dàn dựng kịch bản giả chủ trọ / giả đóng tiền trường. Vì vậy hệ thống bắt buộc phải kiểm tra chéo với lịch sử giao dịch (`nguoi_nhan_da_chuyen_truoc = co`, thiết bị quen thuộc) trước khi cho phép gỡ giữ.
3. **Thiết kế nhóm `chua_ro` phục vụ luồng "Hỏi lại một câu" (Clarification):**
   - **`M0004`, `M0012`, `M0013`, `M0016`, `M0022`, `M0024`,`M0039`,`M0040`:** Các tin nhắn cực ngắn, cộc lốc ("?", "alo sao ko chuyển đc", "sao bi chan vay ad").
   - *Mục đích thiết kế:* Đây là bộ mẫu lý tưởng để kiểm thử hành vi của Agent: không được vội vàng phán đoán hay mở khóa bừa bãi, mà phải kích hoạt luồng **phản hồi một câu hỏi làm rõ** một cách thân thiện, hướng dẫn khách hàng cung cấp thêm lý do chuyển tiền hoặc xác nhận danh tính.

## 5. Ghi chú kỹ thuật & Bảo mật thông tin (Anti-Leak)
- Cột `nhom_that` là đáp án đánh giá (ground-truth).
- **Quy tắc bảo mật công cụ:** Khi lập trình công cụ truy vấn dữ liệu (`get_transaction`, `get_message`), **tuyệt đối không trả trường `nhom_that` cho Agent/Model** để đảm bảo tính khách quan của quá trình chấm benchmark.
