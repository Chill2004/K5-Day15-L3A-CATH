# Nguồn câu thử CP2

R01–R06 diễn giải hoặc dịch từ review đã merge. Ngày 27/11/2026, Chử Thị Ánh xác nhận đã đối chiếu và kiểm lại đúng nhãn của 6 review dùng ở đây (stt 144, 93, 130, 157, 220, 204). Xác nhận này chỉ áp dụng cho 6 review đã chọn, không phải toàn bộ bảng 400 review hoặc phép chấm độc lập output. Chưa ghi nhận đối chiếu độc lập Google Play.

Một số nguồn nói về tài khoản bị khóa hoặc tiền đã trừ, rộng hơn lát cắt tạm giữ. Không thêm nguyên nhân nghi gian lận hoặc áp lực chuyển tiền vào nguồn. R06 dùng mục đích trả bảo hiểm làm nhãn gap_that; Ánh xác nhận đã cùng Cường/Trí duyệt đáp án trước khi chốt CP2.

| Câu | stt | App | Ngày | Xử lý |
|---|---|---|---|---|
| R01 | 144 | MoMo | 2026-11-16 | Diễn giải, bỏ lời chửi và chi tiết không cần thiết |
| R02 | 93 | MoMo | 2026-11-17 | Diễn giải, bỏ lời chửi và chi tiết không cần thiết |
| R03 | 130 | TPBank | 2026-09-25 | Diễn giải, bỏ lời chửi và chi tiết không cần thiết |
| R04 | 157 | TPBank | 2026-10-09 | Diễn giải, bỏ lời chửi và chi tiết không cần thiết |
| R05 | 220 | PayPal | 2026-11-15 | Dịch và diễn giải |
| R06 | 204 | Venmo | 2026-11-14 | Dịch và diễn giải |

Tra trích đoạn gốc theo stt trong evidence/reviews_labeled.csv. C01–C12 là tự viết. Không sử dụng SIM-R001–SIM-R006. Chưa chạy eval chính thức hoặc đo độ khớp người chấm.

## Bổ sung CP3 — chỉ thêm câu

- R07 dịch và diễn giải review stt=375, Wise, UK, ngày 12/11/2026: người viết chờ xác minh một tuần, tiền vẫn bị giữ. Không diễn giải từ “scammers” thành bằng chứng người dùng bị kẻ gian thúc chuyển. Chưa ghi nhận Ánh kiểm riêng nguồn mới này.
- C13 tự viết, thử người dùng tự gửi và yêu cầu nhắc lại OTP. Dãy số là mã giả phục vụ kiểm thử, không phải dữ liệu cá nhân hoặc OTP thật.
- Tổng sau bổ sung: 20 câu, gồm 7 câu từ review và 13 câu tự viết; nguồn review 7/20. Giữ nguyên 18 dòng cũ, metric và chuẩn đạt đã chốt.

