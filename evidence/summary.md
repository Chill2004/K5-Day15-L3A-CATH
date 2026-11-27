# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ **Đạt** — CFPB (nhãn cơ quan gắn) + 400 review gắn nhãn tay, cách chọn mẫu và định nghĩa nhãn ghi trước, script trong `evidence/scripts/` | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ **Đạt** — 6 người ngoài nhóm (P1 do Ánh hỏi; P2–P6 do Hà hỏi, Hà xác nhận là người thật, có dùng AI chỉnh câu văn ghi chép — khai ở `docs/ai-usage.md`) | `evidence/interviews/P1.md` … `P6.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ **Đạt** — 21 phản hồi, **N = 20** người có chuyển tiền bằng ví / app ngân hàng (chốt 27/11/2026, 19:26); log đủ câu hỏi + từng câu trả lời (đã bỏ dấu thời gian và liên hệ) | `evidence/survey/questions.md`, `evidence/survey/results.csv`, `evidence/scripts/clean_survey.py` |

## 2. Số chính

- Đào data:
  - **CFPB** (Mỹ), khiếu nại về chuyển tiền / ví điện tử nhận 27/11/2025–27/11/2026: lừa đảo + giao dịch trái phép **18.701/38.899 (48,1%)**; thêm "không dùng được tiền trong ví" → **22.841/38.899 (58,7%)**. Nhãn do CFPB gắn.
  - **Review Google Play 1–2 sao**, 15 app ví / ngân hàng, mẫu ngẫu nhiên 400 (seed 42), đã gắn nhãn và Cường kiểm 400/400: bị khoá / giữ **hoặc** lừa đảo **48/400 (12,0%)** — VN **13/200 (6,5%)**, Mỹ/Anh **35/200 (17,5%)**; hỗ trợ kém 53/400 (13,2%).
  - Bối cảnh VN (không tính là bằng chứng đạt ngưỡng): MoMo cảnh báo gần 29.000 giao dịch bất thường mỗi ngày; thiệt hại lừa đảo trực tuyến trên 6.000 tỷ đồng 11 tháng đầu 2025 (Bộ Công an) — nguồn ở `spec.md` §2.
- Phỏng vấn (6 người ngoài nhóm, 27/11/2026): **5/6** kể được một lần giao dịch bị ví giữ hoặc chặn vì nghi rủi ro trong 1 tháng qua (P2–P6); P1 gặp giao dịch treo và hỗ trợ chậm nhưng chưa xác nhận bị giữ vì nghi gian lận. Mỗi người khớp một nhóm trong thiết kế: gấp thật (P2 chủ shop chuyển cọc hàng lúc 21h30, P5 phụ huynh đóng học phí sát hạn), bị giục (P3 hưu trí bị giả công an, P6 sinh viên bị lừa nạp tiền làm nhiệm vụ), bị chiếm tài khoản (P4). Lần gần nhất mất **10–30 phút** (P2 30 · P3 20 · P4 25 · P5 15 · P6 10); P1 khoảng 40 phút chờ nhân viên. Giới hạn: 5/6 do một người hỏi trong cùng một tối, mẫu nhỏ, không ngẫu nhiên.
- Khảo sát (N = 20 người dùng ví / app ngân hàng; 9 người đi làm, 9 học viên AI20K, 2 sinh viên khác):
  - **13/20 (65%)** có giao dịch bị ứng dụng tạm giữ / chặn / bắt xác minh thêm trong 3 tháng qua (5 người trong 1 tháng qua, 8 người 1–3 tháng trước).
  - Trong 13 người bị giữ: **11/13 đã liên hệ hỗ trợ** (chat trong ứng dụng 9, gọi tổng đài 7, ra quầy 5 — chọn nhiều); thời gian xử lý: dưới 5 phút 1 · **5–30 phút 8** · 30 phút–2 giờ 1 · hơn 2 giờ / sang ngày khác 3; hỗ trợ giải quyết được 8, **chỉ một phần 5**.
  - **11/20 (55%)** bản thân hoặc người thân bị giục chuyển tiền gấp trong 1 tháng qua; trong 11 người này **3 người đã chuyển tiền**, 5 tự nhận ra, 3 được người khác / ứng dụng cảnh báo.
  - Giới hạn: mẫu thuận tiện (bạn bè, người thân, bạn cùng khoá của nhóm), không ngẫu nhiên — tỉ lệ không đại diện cho mọi người dùng ví; câu 5 tính cả "bắt xác minh thêm", rộng hơn "bị giữ vì nghi lừa đảo". Cần nhóm xác nhận không có thành viên CATH trong 20 người.

Phỏng vấn nhiều vai thì đếm theo từng vai, không cộng chung.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Học viên cùng khóa, người dùng ví | Một phần: giao dịch treo, hỗ trợ chậm; chưa xác nhận giữ vì nghi gian lận | Khoảng 2 | Khoảng 40 phút chờ nhân viên; khoảng 2 ngày tới hoàn tiền | Không chuyển lặp, lưu ảnh, chat hỗ trợ, nhờ bạn tạm ứng; sau đó ưu tiên ngân hàng |
| P2 | Chủ shop bán quần áo online | Có: chuyển cọc hàng gấp ngoài giờ bị giữ, bot bảo chờ 24h gây nguy cơ mất đơn | Khoảng 3–4 | Khoảng 30 phút | Gửi ảnh lệnh giữ cho đối tác, gọi hotline liên tục giục mở |
| P3 | Cán bộ hưu trí (62 tuổi) | Có: bị giả danh công an dọa bắt, thao túng tâm lý giục chuyển tiền gấp | 1 | Khoảng 20 phút | Con gái can thiệp ngăn chặn, gỡ bớt liên kết tài khoản |
| P4 | Nhân viên IT | Có: bị đăng nhập thiết bị lạ, hack trừ tiền lúc đêm; bot phản hồi bài mẫu | 1 | Khoảng 25 phút | Tự vào app ngân hàng ngắt liên kết, gọi tổng đài khẩn cấp |
| P5 | Nhân viên văn phòng / phụ huynh | Có: chuyển học phí hạn chót 17h bị giữ vì tài khoản trường mới | 1 | Khoảng 15 phút | Chụp thông báo trường tải lên chat, xác thực OTP bổ sung |
| P6 | Sinh viên tìm việc online | Có: suýt bị lừa cọc nhiệm vụ Telegram; app giữ tiền và hiện cảnh báo | 1 | Khoảng 10 phút | Đọc cảnh báo của ví, tra cứu kiểm tra chéo và hủy giao dịch |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. *"nhưng cskh không có ai hỗ trợ qua kênh chat, ticket mở hơn 12 tiếng không thấy phản hồi. tiền bị momo giữ không thể rút"* — MoMo, Google Play VN, 1★, 23/11/2026
2. *"tk ko làm gì cũng khóa vĩnh viễn , k có thời gian ra quầy đâu , đang cần gấp mà còn vậy"* — TPBank, Google Play VN, 1★, 12/10/2026 (`reviews_labeled.csv` stt 10)
3. *"I used it to pay my car insurance and they red flagged me and I've been trying for 2 weeks to get it unblocked and they are no help at all"* — Venmo, Google Play US, 1★, 14/11/2026 (stt 204)
4. *"they are complicit with scammers and thieves. had over $8000 stolen and all they said was "there is nothing we can do""* — Cash App, Google Play US, 1★, 26/11/2026 (stt 307)
5. *"They freeze your account and take your money and then sit there for weeks without getting back to you."* — Wise, Google Play UK, 1★, 11/11/2026 (stt 289)
6. *"thỉnh thoảng khi giao dịch bị giữ thì mình ko biết là tiền đã được chuyển chưa"* — khảo sát, câu 11, người dùng ví (`evidence/survey/results.csv`)
7. *"Khi em tôi chuyển tiền xong nó gọi lại cho người ta thì không được nên mới biết là bị lừa"* — khảo sát, câu 11
8. *"Giữ tiền xong không trả về tài khoản người chuyển mà trả về tài khoản người nhận hoặc treo tiền lâu"* — khảo sát, câu 11
9. Lời P1 (phỏng vấn): xem `evidence/interviews/P1.md`.
10. *"Buôn bán gấp từng phút mà ví cứ đè lúc đêm muộn ra giữ tiền rồi bot trả lời tự động bảo chờ 24h thì khách hàng bỏ đi hết"* — P2, chủ shop online (`evidence/interviews/P2.md`)
11. *"Lúc nó dọa bắt đi tù sợ toát mồ hôi hột, app chặn lại mình còn bực mình bảo sao ví làm phiền thế"* — P3, hưu trí 62 tuổi (`evidence/interviews/P3.md`)

## 4. Các nguồn có khớp nhau không

- **Data nói:** khoá / giữ tiền và lừa đảo là nhóm khiếu nại lớn ở Mỹ/Anh (CFPB 48,1%; review 17,5%) và hỗ trợ kém đi kèm (review Mỹ/Anh 19,5%). Ở VN tỉ lệ thấp hơn nhiều (review 6,5%) — review VN 1–2 sao chủ yếu là lỗi đăng nhập, xác thực, lag.
- **Người dùng nói:** 5/6 người phỏng vấn kể được một lần bị giữ trong tháng qua, lần gần nhất mất 10–30 phút; P2 gặp bot "chờ 24 giờ", P4 gặp bot "hỏi lý do vòng vo" — **khớp** phần "hỗ trợ chậm / chung chung". Ba điều **ngược với nhóm nghĩ**: (1) người đang bị lừa (P3) cáu gắt đòi app mở chặn ngay, không tự nhận ra → ủng hộ luật "phân vân thì giữ" và không coi lời nài nỉ là căn cứ; (2) người bán gấp thật (P2) sợ bị giữ tiền làm trễ hẹn hơn là sợ bị lừa → nhánh `gap_that` phải gửi xác thực ngay, không vòng vo; (3) người bị chiếm tài khoản (P4) muốn **khoá ví ngay trong 5 giây** — thiết kế của nhóm chỉ chuyển tư vấn viên, khoá ví là bản nháp chờ duyệt → đây là chỗ đánh đổi có chủ đích (khoá nhầm cũng gây hại, nên cần người duyệt); nếu làm tiếp thì đo thời gian từ lúc chuyển người tới lúc tư vấn viên khoá.
- **Khảo sát VN nói:** 13/20 từng bị giữ giao dịch trong 3 tháng, 11/13 phải liên hệ hỗ trợ, 5/13 chỉ được giải quyết một phần; 11/20 bị giục chuyển tiền và 3 người đã chuyển.
- **Khớp phần lớn, lệch ở review VN.** Khảo sát cho thấy pain có thật ở VN, trong khi review VN chỉ 6,5% nhắc tới. Giải thích hợp lý nhất: người dùng VN gặp chuyện bị giữ nhưng hiếm khi viết review 1–2 sao về nó (review VN 1–2 sao tập trung vào lỗi đăng nhập, xác thực, lag); hướng ngược lại — khảo sát cao vì mẫu thuận tiện và câu hỏi rộng — cũng có thể góp phần. Hai nguồn đều cho thấy **hỗ trợ chậm / chỉ giải quyết một phần** là chỗ đau chung.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md` (ngưỡng ≥10% review 1–2 sao gắn nhãn khoá/giữ hoặc lừa đảo, và ≥2/3 người phỏng vấn kể được một lần trong 1 tháng qua):
- Phần review: **đúng ở cả mẫu (12,0%) và Mỹ/Anh (17,5%), chưa đúng ở VN (6,5%)**.
- Phần phỏng vấn: **đúng** — 5/6 người kể được một lần trong 1 tháng qua (ngưỡng ≥2/3).
- Khảo sát (nguồn kiểm lại, không thuộc ngưỡng giả thuyết ban đầu): 13/20 bị giữ, 11/13 phải liên hệ hỗ trợ, 11/20 bị giục chuyển tiền → **ủng hộ giả thuyết ở VN**.
- Kết luận (cập nhật 27/11/2026, sau khảo sát): **giả thuyết đúng, với giới hạn** — pain có thật ở Mỹ/Anh (CFPB, review) và ở VN (khảo sát 20 người); số review VN thấp không phản bác vì người dùng VN ít viết review về chuyện này. Phỏng vấn 6 người ngoài nhóm (5/6 gặp đúng pain) củng cố thêm. Giới hạn: khảo sát và phỏng vấn đều là mẫu thuận tiện; P2–P6 do một người hỏi trong cùng một tối, ghi chép có AI chỉnh câu văn.
- Điều vẫn chưa biết: tỉ lệ giao dịch bị giữ trên toàn bộ người dùng ví (MoMo chỉ công bố số giao dịch bị cảnh báo); khảo sát mẫu thuận tiện nên chưa dùng làm tỉ lệ toàn quốc.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên cùng khóa, người dùng ví ngoài nhóm (P1) | 18:30 ngày 27/11/2026 (UTC+7) | Đã phỏng vấn; Ánh xác nhận ngoài nhóm và đồng ý dùng ghi chép ẩn danh |
| Chủ shop bán quần áo online (P2) | 19:15 ngày 27/11/2026, trực tiếp | Đã phỏng vấn (Hà) |
| Cán bộ hưu trí 62 tuổi (P3) | 20:00 ngày 27/11/2026, trực tiếp | Đã phỏng vấn (Hà) |
| Nhân viên IT 29 tuổi (P4) | 20:30 ngày 27/11/2026, trực tuyến | Đã phỏng vấn (Hà) |
| Nhân viên văn phòng, phụ huynh (P5) | 21:00 ngày 27/11/2026, trực tiếp | Đã phỏng vấn (Hà) |
| Sinh viên năm cuối 22 tuổi (P6) | 21:30 ngày 27/11/2026, trực tuyến | Đã phỏng vấn (Hà) |
