# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu người dùng:
  - `nguoi_lon_tuoi_bi_giuc`: share 35%, 1.2 phiên / người / tháng, 5 lượt hỏi / phiên. Nguồn: Giả định của nhóm, kịch bản lấy từ phỏng vấn P1–P6 (mẫu nhỏ).
  - `chu_shop_nho_gap_that`: share 50%, 3.2 phiên / người / tháng, 2 lượt hỏi / phiên. Nguồn: Giả định của nhóm, tham khảo phỏng vấn P1–P6 (mẫu nhỏ).
  - `nguoi_bi_chiem_tai_khoan`: share 15%, 1.0 phiên / người / tháng, 3 lượt hỏi / phiên. Nguồn: Giả định của nhóm, tham khảo phỏng vấn P1–P6 (mẫu nhỏ).
- **Số người dùng thật** 3 kịch bản: thấp **30.350** · cơ sở **66.770** · cao **121.400**. Nguồn: Theo Ngân hàng Nhà nước (Tạp chí Ngân hàng, 19/11/2025), có gần 30,35 triệu ví điện tử đang hoạt động. Tỉ lệ người dùng gặp giao dịch bị giữ cần hỗ trợ ước tính 0.1% – 0.4%/tháng (tự ước tính, giả định của nhóm do chưa có thống kê riêng cho ví bị giữ).
- **Giá** 2 mức model (Bảng giá BTC cung cấp ngày 25/11/2026):
  - `gemini-3.1-flash-lite`: vào 0.25 · ra 1.50 $/1M tokens
  - `gemini-3.8-flash`: vào 1.50 · ra 7.50 $/1M tokens (áp dụng từ 01/01/2027)
- **Tỷ giá:** 1 USD = 26.030 ₫ (Tỷ giá bán ra tại Vietcombank, xem ngày 27/11/2026).
- **Tỉ lệ đạt** dùng để tính: Chờ kết quả lượt `run-2` từ eval.
- Đo token trên model Gemini, tính giá model `gemini-3.1-flash-lite` và `gemini-3.8-flash`.

## 2. Kết quả mô phỏng

*(Chạy `python run.py simulate --rate-from eval/run-2.csv` sau khi chấm xong lượt 2, rồi dán bảng từ `cost/simulate-N-summary.md` vào đây)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (30.350 người) | / tháng — cơ sở (66.770 người) | / tháng — cao (121.400 người) | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| gemini-3.1-flash-lite | *(chờ chạy simulate)* | *(chờ chạy simulate)* | *(chờ chạy simulate)* | *(chờ chạy simulate)* | *(chờ chạy simulate)* | *(chờ chạy simulate)* |
| gemini-3.8-flash | *(chờ chạy simulate)* | *(chờ chạy simulate)* | *(chờ chạy simulate)* | *(chờ chạy simulate)* | *(chờ chạy simulate)* | *(chờ chạy simulate)* |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): Giảm thiểu rủi ro bị lừa đảo (trung bình thiệt hại lừa đảo trực tuyến tại VN hàng triệu đồng/vụ) và tiết kiệm hàng chục phút chờ đợi hoang mang cho người dùng khi tiền bị tạm giữ.
- Chi phí model / người / tháng (cơ sở): Dự kiến chỉ khoảng vài chục đến vài trăm đồng / người dùng / tháng.
- **Kết luận một dòng — đáng làm không:** **RẤT ĐÁNG LÀM** vì chi phí vận hành AI cực nhỏ so với giá trị tài sản bảo vệ được cho người dùng và khoản chi phí nhân sự tổng đài viên tiết kiệm được hàng tháng.

## 4. Phân tích sâu: Tiết kiệm giờ công tư vấn viên (CSKH)

> Khung `simulate.py` chỉ tính chi phí gọi API của Model. Dưới đây là phân tích chi phí nhân sự thực tế theo yêu cầu của CP4.

### 4.1. Đơn giá giờ công tư vấn viên
- **Nguồn lương:** CareerLink (cập nhật 30/05/2026, https://www.careerlink.vn/cam-nang-viec-lam/tu-van-nghe-nghiep/tong-dai-vien-la-lam-gi), vị trí chuyên viên CSKH / tổng đài viên có 1–3 năm kinh nghiệm dao động từ 10 – 15 triệu đồng/tháng (chỉ tham khảo từ tin tuyển dụng).
- **Giả định tính toán:** Lấy mức lương trung bình **12.500.000 VNĐ/tháng**.
- Quy chuẩn thời gian làm việc: 22 ngày/tháng × 8 giờ/ngày × 60 phút = 10.560 phút/tháng.
- **Đơn giá:**
  $$\text{Đơn giá mỗi phút} = \frac{12.500.000 \text{ ₫}}{10.560 \text{ phút}} \approx \mathbf{1.184 \text{ ₫/phút}} \quad (\approx 71.023 \text{ ₫/giờ})$$
- **Thời gian xử lý trung bình:** Giả định **7 phút/ca** (tự ước tính từ phỏng vấn P1–P6). Chi phí nhân sự xử lý: $7 \times 1.184 \approx 8.288 \text{ ₫/ca}$.

### 4.2. So sánh: Không có AI vs. Có AI (Kịch bản cơ sở: 66.770 người dùng/tháng)
- **Tổng số phiên yêu cầu hỗ trợ / tháng:**
  $$\text{Số phiên} = 66.770 \times (35\% \times 1.2 + 50\% \times 3.2 + 15\% \times 1.0) = 66.770 \times 2.17 \approx \mathbf{144.891 \text{ phiên/tháng}}$$
- **Tỉ lệ chuyển người (handoff rate) khi có AI:**
  - *Cách 1 (Tính theo phiên — dùng cho bảng chi phí):* Vì nhóm chủ shop gấp thật có tần suất cao (3,2 phiên/tháng) mà tỉ lệ chuyển người thấp (25%), nên tính trọng số theo phiên:
    $$\text{Tỉ lệ chuyển theo phiên} = \frac{0.35 \times 1.2 \times 85\% + 0.50 \times 3.2 \times 25\% + 0.15 \times 1.0 \times 95\%}{0.35 \times 1.2 + 0.50 \times 3.2 + 0.15 \times 1.0} = \frac{0.8995}{2.17} \approx \mathbf{41,5\%}$$
  - *Cách 2 (Tính bình quân theo người dùng):* $35\% \times 85\% + 50\% \times 25\% + 15\% \times 95\% = 56,5\%$.
  - Ở bảng dưới, ta áp dụng tỉ lệ theo phiên (**41,5%**) để khớp chính xác với tổng số 144.891 phiên thực tế cần xử lý.

| Tiêu chí | Kịch bản 1: Không có AI (100% người thật) | Kịch bản 2: Có AI hỗ trợ (Chỉ 41,5% phiên chuyển người) | Mức chênh lệch / Tiết kiệm |
|---|---:|---:|---:|
| **Số ca vào tư vấn viên** | 144.891 ca/tháng | 60.060 ca/tháng | **Giảm 84.831 ca** (giảm 58,5%) |
| **Tổng số phút xử lý** | 1.014.237 phút | 420.420 phút | **Tiết kiệm 593.817 phút** |
| **Tổng giờ công nhân sự** | 16.904 giờ/tháng | 7.007 giờ/tháng | **Tiết kiệm 9.897 giờ công** (~56 nhân viên full-time) |
| **Chi phí nhân sự** | **1.200.856.000 ₫/tháng** | **497.777.000 ₫/tháng** | **Tiết kiệm 703.079.000 ₫/tháng** |
| **Chi phí gọi Model AI** | 0 ₫ | *(ước tính, chưa đo — token đang 0 do chờ chạy model thật)* | Chi phí vận hành AI rất nhỏ |
| **TỔNG CHI PHÍ VẬN HÀNH** | **~1,201 tỷ ₫/tháng** | **~498 triệu ₫/tháng** *(chưa gồm chi phí model)* | **TIẾT KIỆM RÒNG ~703 TRIỆU ₫/THÁNG** *(chưa trừ chi phí model)* |

---
*Báo cáo được hoàn thiện bởi: Nguyễn Thị Thu Hà (CATH Track E3).*
