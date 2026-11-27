# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu người dùng:
  - `nguoi_lon_tuoi_bi_giuc`: share 35%, 1.2 phiên / người / tháng, 5 lượt hỏi / phiên. Nguồn: Giả định của nhóm, kịch bản lấy từ phỏng vấn P1–P6 (mẫu nhỏ).
  - `chu_shop_nho_gap_that`: share 50%, 3.2 phiên / người / tháng, 2 lượt hỏi / phiên. Nguồn: Giả định của nhóm, tham khảo phỏng vấn P1–P6 (mẫu nhỏ).
  - `nguoi_bi_chiem_tai_khoan`: share 15%, 1.0 phiên / người / tháng, 3 lượt hỏi / phiên. Nguồn: Giả định của nhóm, tham khảo phỏng vấn P1–P6 (mẫu nhỏ).
- **Số người dùng thật** 3 kịch bản: thấp **30.350** · cơ sở **66.770** · cao **121.400**. Nguồn: Theo Ngân hàng Nhà nước (Tạp chí Ngân hàng, 19/11/2025, https://tapchinganhang.gov.vn/phat-trien-thi-truong-vi-dien-tu-gop-phan-thuc-day-thanh-toan-so-va-chuyen-doi-so-16719.html), có gần 30,35 triệu ví điện tử đang hoạt động trên gần 49,57 triệu ví kích hoạt. Tỉ lệ người dùng gặp giao dịch bị giữ cần hỗ trợ ước tính 0.1% – 0.4%/tháng (tự ước tính, giả định của nhóm do chưa có thống kê riêng cho ví bị giữ).
- **Giá** 2 mức model (Bảng giá BTC cung cấp ngày 25/11/2026):
  - `gemini-3.1-flash-lite`: vào 0.25 · ra 1.50 $/1M tokens
  - `gemini-3.8-flash`: vào 1.50 · ra 7.50 $/1M tokens (áp dụng từ 01/01/2027)
- **Tỷ giá:** 1 USD = 26.030 ₫ (Tỷ giá bán ra tại Vietcombank, xem ngày 27/11/2026).
- **Tỉ lệ đạt** dùng để tính: **15/20 (75%)**, lượt `run-2@20261127-215329` (Ánh chấm tay). Lượt 1 là 12/20 (60%). Cả hai lượt **đều chưa đạt chuẩn 80%** của `spec.md` §7 — số chi phí / task thành công bên dưới tính trên 75%, không coi như đạt 100%.
- **Token đo trên model `gemini-3.1-flash-lite`, tính giá cho cả 2 model** (`gemini-3.1-flash-lite` và `gemini-3.8-flash`). Model khác có thể tách token khác nên số token thật của `gemini-3.8-flash` có thể lệch nhẹ so với số đo.

## 2. Kết quả mô phỏng

Nguồn: `cost/simulate-1-summary.md` (`simulate-1@20261127-230211`, 50 phiên, seed 42, sinh bằng `python run.py simulate`, không sửa tay). **2/50 phiên lỗi không tính vào trung bình** → trung bình lấy trên 48 phiên, không chạy lại để che. Hai phiên lỗi là **S042 và S047** (đều persona `nguoi_lon_tuoi_bi_giuc`, đều lỗi ở lượt T3): **HTTP 503 `UNAVAILABLE`** từ API Gemini ("This model is currently experiencing high demand" — quá tải phía nhà cung cấp), không phải 429 hay lỗi mã của nhóm. Hai phiên này chạy rất lâu (≈ 204–231 giây) trước khi báo lỗi.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| nguoi_lon_tuoi_bi_giuc | 13 | 5 | 6.902 | 734 | 5,0 | 8,0 |
| chu_shop_nho_gap_that | 27 | 2 | 2.761 | 292 | 2,0 | 3,2 |
| nguoi_bi_chiem_tai_khoan | 8 | 3 | 4.141 | 441 | 3,0 | 5,0 |

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | / tháng — thấp (30.350 người) | / tháng — cơ sở (66.770 người) | / tháng — cao (121.400 người) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0,25 · ra 1,5 $/1M) | $0,0017 (≈ 44 ₫) | $0,0022 (≈ 58 ₫) | $0,00075 (≈ 20 ₫) | $98,51 (≈ 2.564.167 ₫) | $216,72 (≈ 5.641.168 ₫) | $394,03 (≈ 10.256.670 ₫) | $0,0032 (≈ 84 ₫) |
| gemini-3.8-flash (vào 1,5 · ra 7,5 $/1M) | $0,0094 (≈ 246 ₫) | $0,0126 (≈ 328 ₫) | $0,0042 (≈ 110 ₫) | $552,76 (≈ 14.388.461 ₫) | $1.216,08 (≈ 31.654.613 ₫) | $2.211,06 (≈ 57.553.842 ₫) | $0,0182 (≈ 474 ₫) |

- Token **đo trên `gemini-3.1-flash-lite`**, giá **tính cho cả 2 model** (số token của `gemini-3.8-flash` là suy ra, chưa đo riêng).
- Tỉ lệ đạt 75% (15/20, `run-2`); lượt 1 là 12/20 (60%); chưa đạt chuẩn 80%.
- Tỷ giá 1 USD = 26.030 ₫ (Vietcombank, xem 27/11/2026).

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): Giảm thiểu rủi ro bị lừa đảo (trung bình thiệt hại lừa đảo trực tuyến tại VN hàng triệu đồng/vụ) và tiết kiệm hàng chục phút chờ đợi hoang mang cho người dùng khi tiền bị tạm giữ.
- Chi phí model / người / tháng (cơ sở, đo): ≈ 84 ₫ với `gemini-3.1-flash-lite`, ≈ 474 ₫ với `gemini-3.8-flash`.
- **Kết luận một dòng — đáng làm không:** **ĐÁNG LÀM về chi phí**: chi phí model chỉ bằng ≈ 0,8% (flash-lite) đến ≈ 4,5% (3.8-flash) khoản giờ công tư vấn viên tiết kiệm được (mục 4). **Điều kiện:** tỉ lệ chuyển người theo phiên 41,5% là giả định của nhóm; AI mới đạt 75% (< chuẩn 80%), nên phần tiết kiệm là mức tối đa nếu AI xử lý đúng, chưa phải số đã chứng minh.

## 4. Phân tích sâu: Tiết kiệm giờ công tư vấn viên (CSKH)

> Khung `simulate.py` chỉ tính chi phí gọi API của Model. Dưới đây là phân tích chi phí nhân sự thực tế theo yêu cầu của CP4.

### 4.1. Đơn giá giờ công tư vấn viên
- **Nguồn lương:** CareerLink (cập nhật 30/05/2026, https://www.careerlink.vn/cam-nang-viec-lam/tu-van-nghe-nghiep/tong-dai-vien-la-lam-gi), vị trí chuyên viên CSKH / tổng đài viên có 1–3 năm kinh nghiệm dao động từ 10 – 15 triệu đồng/tháng (chỉ tham khảo từ tin tuyển dụng).
- **Giả định tính toán:** Lấy mức lương trung bình **12.500.000 VNĐ/tháng**.
- Quy chuẩn thời gian làm việc: 22 ngày/tháng × 8 giờ/ngày × 60 phút = 10.560 phút/tháng.
- **Đơn giá:**
  $$\text{Đơn giá mỗi phút} = \frac{12.500.000 \text{ ₫}}{10.560 \text{ phút}} \approx \mathbf{1.184 \text{ ₫/phút}} \quad (\approx 71.023 \text{ ₫/giờ})$$
- **Thời gian xử lý trung bình:** Giả định **7 phút/ca (tự ước tính)**. Nhóm không có số đo thời gian tư vấn viên xử lý một ca; số khảo sát (5–30 phút) và phỏng vấn (10–30 phút) là thời gian người dùng mất, gồm cả lúc chờ máy, nên không dùng thay được. Chi phí nhân sự xử lý: $7 \times 1.184 \approx 8.288 \text{ ₫/ca}$.

### 4.2. So sánh: Không có AI vs. Có AI (Kịch bản cơ sở: 66.770 người dùng/tháng)
- **Tổng số phiên yêu cầu hỗ trợ / tháng:**
  $$\text{Số phiên} = 66.770 \times (35\% \times 1.2 + 50\% \times 3.2 + 15\% \times 1.0) = 66.770 \times 2.17 \approx \mathbf{144.891 \text{ phiên/tháng}}$$
- **Tỉ lệ chuyển người (handoff rate) khi có AI:**
  - *Cách 1 (Tính theo phiên — dùng cho bảng chi phí):* Vì nhóm chủ shop gấp thật có tần suất cao (3,2 phiên/tháng) mà tỉ lệ chuyển người thấp (25%), nên tính trọng số theo phiên:
    $$\text{Tỉ lệ chuyển theo phiên} = \frac{0.35 \times 1.2 \times 85\% + 0.50 \times 3.2 \times 25\% + 0.15 \times 1.0 \times 95\%}{0.35 \times 1.2 + 0.50 \times 3.2 + 0.15 \times 1.0} = \frac{0.8995}{2.17} \approx \mathbf{41,5\%}$$
  - *Cách 2 (Tính bình quân theo người dùng):* $35\% \times 85\% + 50\% \times 25\% + 15\% \times 95\% = 56,5\%$.
  - Ở bảng dưới, ta áp dụng tỉ lệ theo phiên (**41,5%**) để khớp chính xác với tổng số 144.891 phiên thực tế cần xử lý.

| Tiêu chí (kịch bản cơ sở) | Kịch bản 1: Không có AI (100% người thật) | Kịch bản 2: Có AI hỗ trợ (chỉ 41,5% phiên chuyển người) | Mức chênh lệch / Tiết kiệm |
|---|---:|---:|---:|
| **Số ca vào tư vấn viên** | 144.891 ca/tháng | 60.060 ca/tháng | **Giảm 84.831 ca** (giảm 58,5%) |
| **Tổng số phút xử lý** (7 phút/ca, tự ước tính) | 1.014.237 phút | 420.420 phút | **Tiết kiệm 593.817 phút** |
| **Tổng giờ công nhân sự** | 16.904 giờ/tháng | 7.007 giờ/tháng | **Tiết kiệm 9.897 giờ công** (~56 nhân viên full-time) |
| **Chi phí nhân sự** | 1.200,9 triệu ₫/tháng | 497,8 triệu ₫/tháng | Tiết kiệm 703,1 triệu ₫/tháng |
| **Chi phí gọi model (đo, mục 2)** | 0 ₫ | 5,6 triệu ₫ (flash-lite) · 31,7 triệu ₫ (3.8-flash) | — |
| **TỔNG CHI PHÍ VẬN HÀNH** | **≈ 1.200,9 triệu ₫/tháng** | **≈ 503,4 triệu ₫** (flash-lite) · **≈ 529,4 triệu ₫** (3.8-flash) | **TIẾT KIỆM RÒNG ≈ 697,4 triệu** (flash-lite) · **≈ 671,4 triệu ₫/tháng** (3.8-flash) |

**Độ nhạy theo số phút/ca (kịch bản cơ sở, đã trừ chi phí model đo ở mục 2):** 5 phút/ca → tiết kiệm ròng ≈ 496,6 triệu ₫/tháng (flash-lite) · ≈ 470,5 triệu (3.8-flash); 7 phút → ≈ 697,4 · ≈ 671,4 triệu; 15 phút → ≈ 1,50 tỷ · ≈ 1,47 tỷ ₫. Kết luận "đáng làm" không đổi: tiết kiệm ròng chỉ về 0 khi mỗi ca chuyển người mất dưới ≈ 0,3 phút (3.8-flash) hoặc ≈ 0,06 phút (flash-lite).

### 4.3. Ba kịch bản người dùng (triệu ₫ / tháng)

Số phiên = số người × 2,17; ca chuyển người = số người × 0,8995; mỗi ca chuyển người mất 7 phút (tự ước tính) × 1.184 ₫/phút. Chi phí model lấy từ bảng mục 2.

| Kịch bản | Không có AI (giờ công) | Có AI: giờ công + model flash-lite | Có AI: giờ công + model 3.8-flash | Tiết kiệm ròng (flash-lite) | Tiết kiệm ròng (3.8-flash) |
|---|---:|---:|---:|---:|---:|
| Thấp (30.350 người) | 545,8 | 226,3 + 2,6 = **228,8** | 226,3 + 14,4 = **240,6** | **317,0** | **305,2** |
| Cơ sở (66.770 người) | 1.200,9 | 497,8 + 5,6 = **503,4** | 497,8 + 31,7 = **529,4** | **697,4** | **671,4** |
| Cao (121.400 người) | 2.183,4 | 905,0 + 10,3 = **915,3** | 905,0 + 57,6 = **962,6** | **1.268,1** | **1.220,8** |

### 4.4. Giả định và giới hạn (ghi trung thực)

- **Số phút / ca chuyển người = 7 phút (tự ước tính)**: nhóm không có số đo thời gian tư vấn viên xử lý một ca (số khảo sát và phỏng vấn là thời gian người dùng mất, không dùng thay được). **Tỉ lệ chuyển người theo persona (85% · 25% · 95%)** là **giả định của nhóm** (tham khảo phỏng vấn P1–P6, mẫu nhỏ), chưa đo. Lương 12,5 triệu/tháng là mức giữa khoảng 10–15 triệu của CareerLink (chỉ tham khảo).
- Chi phí model là số **đo** (token trên `gemini-3.1-flash-lite`); 2/50 phiên lỗi không tính vào trung bình.
- AI mới đạt 15/20 (75%), lượt 1 là 12/20 (60%), cả hai chưa đạt chuẩn 80%. Phần tiết kiệm giờ công giả định AI xử lý đúng các ca không chuyển người, nên là **mức tối đa**, chưa trừ chi phí xử lý lại các ca AI trả lời sai.
- Chưa tính chi phí hạ tầng, nhân sự phát triển và chi phí kiểm duyệt.

---
*Báo cáo được hoàn thiện bởi: Nguyễn Thị Thu Hà (CATH Track E3).*
