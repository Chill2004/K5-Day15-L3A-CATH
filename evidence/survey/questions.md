# Khảo sát — giao dịch bị tạm giữ và bị giục chuyển tiền (Track E3)

> Guide bước 1.2. Ngưỡng: **≥20 người ngoài nhóm, đúng người dùng** (có chuyển tiền bằng ví / app ngân hàng), giữ log đủ câu hỏi và từng câu trả lời.
> Mục đích: kiểm lại bằng chứng đào data ở Việt Nam — review VN 1–2 sao chỉ 6,5% nhắc tới bị khoá/giữ hoặc lừa đảo (`evidence/data-mining.md`).
> Hỏi **hành vi đã xảy ra**, không hỏi "có thích không". **Không hỏi số tiền, số tài khoản, số dư, thu nhập.** Không thu tên / email (trừ câu 11, tự nguyện).
> Thành viên nhóm CATH **không** tự trả lời (không tính là bằng chứng).

- Tạo form: chạy `evidence/survey/tao_form.gs` trong Google Apps Script (hướng dẫn ở đầu file đó), hoặc chép tay các câu dưới đây.
- Kênh đã gửi: __ · Mở lúc: __ · Chốt lúc: __
- Kết quả: xuất CSV từ Google Form → **xoá cột thời gian và câu 11 (liên hệ)** → lưu `evidence/survey/results.csv`. Bản gốc có thông tin liên hệ **không commit**.

## Câu hỏi

| # | Câu hỏi | Kiểu trả lời | Bắt buộc |
|---|---|---|---|
| 1 | Trong 3 tháng qua, bạn có chuyển tiền bằng ví điện tử hoặc app ngân hàng không? | Có · Không (→ kết thúc) | Có |
| 2 | Bạn là: | Học viên AI20K · Sinh viên khác · Người đi làm · Khác | Có |
| 3 | Độ tuổi | Dưới 22 · 22–30 · 31–45 · Trên 45 | Có |
| 4 | Bạn hay chuyển tiền bằng ứng dụng nào? | Chọn nhiều: MoMo · ZaloPay · ShopeePay · App ngân hàng (Vietcombank, MB, Techcombank…) · Khác | Có |
| 5 | Trong 3 tháng qua, có lần nào giao dịch của bạn bị ứng dụng **tạm giữ, chặn, hoặc bắt xác minh thêm** (khác với nhập OTP bình thường) không? | Có, trong 1 tháng qua · Có, 1–3 tháng trước · Không · Không nhớ | Có |
| 6 | *(Nếu có ở câu 5)* Lần gần nhất đó, bạn đã làm gì? | Chọn nhiều: Chat với hỗ trợ trong ứng dụng · Gọi tổng đài · Ra quầy / chi nhánh · Chờ tự xử lý · Chuyển bằng cách khác · Bỏ, không chuyển nữa · Khác | Không |
| 7 | *(Nếu có ở câu 5)* Lần đó mất bao lâu thì xong? | Dưới 5 phút · 5–30 phút · 30 phút – 2 giờ · Hơn 2 giờ / sang ngày khác · Không xong, bỏ | Không |
| 8 | *(Nếu có ở câu 5)* Kênh hỗ trợ có giải quyết được cho bạn không? | Giải quyết được · Một phần · Không · Không liên hệ hỗ trợ | Không |
| 9 | Trong 1 tháng qua, bạn hoặc người thân có nhận **cuộc gọi / tin nhắn giục chuyển tiền gấp** không? (tự xưng công an, toà án, ngân hàng, người quen, việc làm online…) | Có, bản thân · Có, người thân · Cả hai · Không · Không nhớ | Có |
| 10 | *(Nếu có ở câu 9)* Khi đó điều gì đã xảy ra? | Không chuyển, tự nhận ra · Không chuyển, được người khác hoặc ứng dụng cảnh báo · Đã chuyển tiền · Không biết | Không |
| 11 | Điều gì làm bạn khó chịu hoặc lo nhất khi giao dịch bị giữ / khi bị giục chuyển tiền? | Đoạn văn | Không |
| 12 | *(Tuỳ chọn)* Bạn có sẵn lòng cho nhóm hỏi thêm 10 phút không? Nếu có, để lại cách liên hệ. | Câu trả lời ngắn | Không |

## Cách đếm (ghi trước khi xem kết quả)

- Mẫu số N = số người trả lời **Có** ở câu 1.
- Số chính: (a) x/N người có giao dịch bị giữ trong 3 tháng qua (câu 5, hai lựa chọn "Có"); (b) x/N người bản thân hoặc người thân bị giục chuyển tiền trong 1 tháng qua (câu 9, ba lựa chọn "Có"); (c) trong số người bị giữ: thời gian xử lý (câu 7) và kênh hỗ trợ có giải quyết được không (câu 8).
- Dưới khoảng 10 người thì chỉ ghi x/n, không ghi %.
- Giới hạn: mẫu là bạn bè, người thân của nhóm (không ngẫu nhiên) — ghi rõ khi báo cáo.
