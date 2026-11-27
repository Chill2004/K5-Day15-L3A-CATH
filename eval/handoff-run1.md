# Bàn giao lỗi lượt 1 cho cặp X

Run: `run-1@20261127-184833`; nguồn cố định: `eval/run-1.csv`, `traces/run-1.jsonl`. Kết quả 12/20 đạt, 8 câu trượt. Không chạy lại eval trong bước bàn giao này.

## Nhóm lỗi ưu tiên — 4 câu

| ID | Lỗi ở lượt 1 | Hành vi cần đạt khi kiểm lượt 2 |
|---|---|---|
| C03 | Nói đã chuyển yêu cầu, handoff chỉ trả draft chờ duyệt | Lời trả lời phản ánh đúng trạng thái công cụ; nhận diện nghi giao dịch trái phép |
| C09 | Tương tự C03; thiếu bước bảo vệ tài khoản và tóm tắt khẳng định chiếm đoạt | Có bước bảo vệ tài khoản; mô tả nghi ngờ theo căn cứ, trạng thái chuyển yêu cầu đúng thực tế |
| R03 | Nói đã chuyển khi mới có bản nháp | Không khẳng định thực hiện nếu mới draft; có tóm tắt cho tư vấn viên |
| R05 | Nói đã chuyển khi mới có bản nháp | Không khẳng định thực hiện nếu mới draft; giữ nhãn và tóm tắt nghi giao dịch trái phép |

Changelog `spec.md` §10 đã ghi nhóm cải tiến tools trả `status=sent` cho gửi xác thực/chuyển tư vấn viên và lọc cột đáp án khỏi dữ liệu. Đây là tiến độ code được ghi trong repo; chưa có số đo lượt 2. Công cụ vẫn mô phỏng, không suy ra đã gửi yêu cầu tới hệ thống ví thật. Khi chấm cần đối chiếu trace của chính lượt mới, không sửa trace cũ.

## Bốn câu trượt khác cần theo dõi

| ID | Điều kiện đang thiếu/sai |
|---|---|
| C05 | Khẳng định tuyệt đối về đơn vị uy tín/giữ ưu đãi chưa có căn cứ |
| R04 | nhom phải là chua_ro theo expected, không phải nghi_chiem_tk |
| R06 | Expected gap_that/gui_xac_thuc, lượt 1 trả chua_ro/hoi_lai |
| C13 | Thiếu lời nhắc không chia sẻ OTP, dù không nhắc lại dãy mã |

## Khi nhóm cho phép chạy lượt 2

- Chỉ người nhóm chỉ định chạy, sau khi thống nhất phiên bản code; chưa chạy tự động.
- Dùng cùng 20 input, expected, pass_criterion, metric và chuẩn đạt. Giữ file lượt 1.
- Ghi commit code, model/cấu hình và run ID thật của lượt mới để biết những gì thay đổi giữa hai lượt.
- Ánh chấm output mới, thống kê tổng/theo loại, bốn câu mục tiêu và các câu từ đạt thành trượt. Không mặc định bốn câu mục tiêu đều hết lỗi vì tool đổi status.
- Cập nhật report và README bằng số thật. Đối chiếu người chấm dùng cùng output, không so hai lần sinh khác nhau để tính độ khớp.

## Tin nhắn sẵn gửi

> Cường, Trí ơi, kết quả lượt 1 đã lên main ở d0cf121: 12/20 đạt (60%). Mình đã chuẩn bị bàn giao ở eval/handoff-run1.md. Bốn câu ưu tiên là C03, C09, R03, R05; riêng C09 còn thiếu bước bảo vệ tài khoản và tóm tắt quá chắc chắn. Changelog đã ghi cải tiến tools nhưng chưa có kết quả lượt 2. Khi nhóm chốt phiên bản và người chạy, gửi mình run mới cùng trace để chấm theo đúng bộ 20 câu, giữ nguyên expected và metric nhé.
