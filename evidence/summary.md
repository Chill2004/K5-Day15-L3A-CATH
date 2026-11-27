# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ **Đạt** — CFPB (nhãn cơ quan gắn) + 400 review gắn nhãn tay, cách chọn mẫu và định nghĩa nhãn ghi trước, script trong `evidence/scripts/` | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ Chưa — mới 1 người (P1) | `evidence/interviews/P1.md`… |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ Chưa — 20 phản hồi, 19 người đúng người dùng (27/11/2026, 19:20); đang thu thêm | `evidence/survey/` |

## 2. Số chính

- Đào data:
  - **CFPB** (Mỹ), khiếu nại về chuyển tiền / ví điện tử nhận 27/11/2025–27/11/2026: lừa đảo + giao dịch trái phép **18.701/38.899 (48,1%)**; thêm "không dùng được tiền trong ví" → **22.841/38.899 (58,7%)**. Nhãn do CFPB gắn.
  - **Review Google Play 1–2 sao**, 15 app ví / ngân hàng, mẫu ngẫu nhiên 400 (seed 42), đã gắn nhãn và Cường kiểm 400/400: bị khoá / giữ **hoặc** lừa đảo **48/400 (12,0%)** — VN **13/200 (6,5%)**, Mỹ/Anh **35/200 (17,5%)**; hỗ trợ kém 53/400 (13,2%).
  - Bối cảnh VN (không tính là bằng chứng đạt ngưỡng): MoMo cảnh báo gần 29.000 giao dịch bất thường mỗi ngày; thiệt hại lừa đảo trực tuyến trên 6.000 tỷ đồng 11 tháng đầu 2025 (Bộ Công an) — nguồn ở `spec.md` §2.
- Phỏng vấn: đã ghi nhận 1 người (P1), có gặp giao dịch treo và hỗ trợ chậm; chưa xác nhận tạm giữ vì nghi gian lận. Chưa đủ ngưỡng ≥3 người ngoài nhóm; cần xác nhận P1 ngoài nhóm. P1 tự khai khoảng 2 lần/tháng, lần gần nhất khoảng 40 phút chờ nhân viên và khoảng 2 ngày tới khi hoàn tiền; chưa có số phút thao tác chủ động. Chi tiết: `evidence/interviews/P1.md`.
- Khảo sát: n = __ · __/__ (__%) …

Phỏng vấn nhiều vai thì đếm theo từng vai, không cộng chung.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Học viên cùng khóa, người dùng ví | Một phần: giao dịch treo, hỗ trợ chậm; chưa xác nhận giữ vì nghi gian lận | Khoảng 2 | Khoảng 40 phút chờ nhân viên; khoảng 2 ngày tới hoàn tiền | Không chuyển lặp, lưu ảnh, chat hỗ trợ, nhờ bạn tạm ứng; sau đó ưu tiên ngân hàng |
| P2 | | | | | |
| P3 | | | | | |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. *"nhưng cskh không có ai hỗ trợ qua kênh chat, ticket mở hơn 12 tiếng không thấy phản hồi. tiền bị momo giữ không thể rút"* — MoMo, Google Play VN, 1★, 23/11/2026
2. *"tk ko làm gì cũng khóa vĩnh viễn , k có thời gian ra quầy đâu , đang cần gấp mà còn vậy"* — TPBank, Google Play VN, 1★, 12/10/2026 (`reviews_labeled.csv` stt 10)
3. *"I used it to pay my car insurance and they red flagged me and I've been trying for 2 weeks to get it unblocked and they are no help at all"* — Venmo, Google Play US, 1★, 14/11/2026 (stt 204)
4. *"they are complicit with scammers and thieves. had over $8000 stolen and all they said was "there is nothing we can do""* — Cash App, Google Play US, 1★, 26/11/2026 (stt 307)
5. *"They freeze your account and take your money and then sit there for weeks without getting back to you."* — Wise, Google Play UK, 1★, 11/11/2026 (stt 289)
6. Lời P1 (phỏng vấn): xem `evidence/interviews/P1.md`.

## 4. Các nguồn có khớp nhau không

- **Data nói:** khoá / giữ tiền và lừa đảo là nhóm khiếu nại lớn ở Mỹ/Anh (CFPB 48,1%; review 17,5%) và hỗ trợ kém đi kèm (review Mỹ/Anh 19,5%). Ở VN tỉ lệ thấp hơn nhiều (review 6,5%) — review VN 1–2 sao chủ yếu là lỗi đăng nhập, xác thực, lag.
- **Người dùng nói:** P1 kể gặp giao dịch treo khoảng 2 lần / tháng, lần gần nhất chờ nhân viên khoảng 40 phút — **khớp** phần "hỗ trợ chậm", nhưng P1 **chưa** xác nhận bị giữ vì nghi gian lận.
- **Khớp một phần.** Lệch ở chỗ VN: data review VN dưới ngưỡng giả thuyết. Có thể do người dùng VN ít viết review về chuyện bị giữ, hoặc do ở VN chuyện này thật sự ít gặp → đang kiểm bằng khảo sát (câu 5, 6, 7) và phỏng vấn thêm.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md` (ngưỡng ≥10% review 1–2 sao gắn nhãn khoá/giữ hoặc lừa đảo, và ≥2/3 người phỏng vấn kể được một lần trong 1 tháng qua):
- Phần review: **đúng ở cả mẫu (12,0%) và Mỹ/Anh (17,5%), chưa đúng ở VN (6,5%)**.
- Phần phỏng vấn: **chưa đủ dữ liệu** (1/3 người, P1 gặp một phần).
- Kết luận tạm (27/11/2026, 19:20): **đúng một phần — pain có thật và lớn ở thị trường Mỹ/Anh; ở VN phải kiểm thêm**. Cập nhật sau khi khảo sát đủ ≥20 người.
- Điều vẫn chưa biết: tỉ lệ người dùng VN thật sự bị giữ giao dịch và phải liên hệ hỗ trợ (p trong công thức impact `spec.md` §2), thời gian chờ (t).

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên cùng khóa, người dùng ví (P1) | 18:30 ngày 27/11/2026 (UTC+7) | Ánh xác nhận đã phỏng vấn; cần xác nhận ngoài nhóm |
