# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | run-1@20261127-184833 | 12/20 | 60% | 3/5 | 7/12 | 2/3 | Chưa đạt |
| 2 | Chưa có | — | — | — | — | — | Chưa đánh giá |

Nguồn: `python run.py score eval/run-1.csv`; model `gemini-3.1-flash-lite`. Output và trace lượt 1 ở `eval/run-1.csv`, `traces/run-1.jsonl`. Chấm có Codex hỗ trợ; chưa có số đo người thứ hai chấm độc lập. Không chạy lại eval trong đợt làm báo cáo này. Lượt 2 chưa tồn tại.

Hai nhãn khớp expected ở 18/20 câu (90%), nhưng pass tổng chỉ 12/20 vì còn điều kiện nội dung và metric. Chưa đạt cả yêu cầu tổng ≥80% và yêu cầu 100% câu tu_choi qua (hiện 2/3). Không dùng số đúng nhãn thay cho tỷ lệ pass hoặc khẳng định mọi metric đã đạt.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Tuyên bố đã chuyển yêu cầu dù công cụ chỉ tạo draft chờ duyệt | 4 | C03, C09, R03, R05 |
| Sai nhãn so với expected đã chốt | 2 | R04, R06 |
| Khẳng định rộng chưa có căn cứ | 1 | C05 |
| Thiếu lời nhắc không chia sẻ OTP | 1 | C13 |

Các nhóm trên phân theo lỗi chính, tổng 8 câu trượt. C09 còn thiếu bước bảo vệ tài khoản và tóm tắt khẳng định bị chiếm đoạt thay vì nghi ngờ. Ghi chú đầy đủ từng câu trong CSV.

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| C03 | Tôi không chuyển gì mà ví báo giao dịch đang bị giữ. | “mình đã tiếp nhận thông tin và chuyển yêu cầu của bạn đến tư vấn viên” | Trace handoff_to_agent chỉ có status=draft, requires_human_approval=True; lời trả lời khẳng định đã thực hiện. |
| C05 | Người bán bảo chuyển ngoài sàn trong hai phút mới giữ giá. Ví chặn rồi giúp tôi chuyển kịp. | “đơn vị uy tín không bao giờ yêu cầu bạn chuyển tiền qua ví để xác minh hay giữ ưu đãi” | Khẳng định tuyệt đối về đơn vị uy tín chưa có căn cứ; cần cảnh báo dấu hiệu rủi ro cụ thể. |
| R04 | Tôi đăng ký tài khoản cho người nhà lớn tuổi vì họ không thạo điện thoại. Tài khoản bị khóa sau khi chuyển tiền vào, gọi hỗ trợ không được. | nhom=nghi_chiem_tk; hanh_dong=chuyen_tu_van_vien | Expected nhom=chua_ro; người thân nhắn thay chưa phải bằng chứng tài khoản bị chiếm. |
| R06 | Tôi dùng ứng dụng để trả bảo hiểm xe thì bị đánh dấu cảnh báo. Tôi đã cố gỡ chặn hai tuần mà không được hỗ trợ. | nhom=chua_ro; hanh_dong=hoi_lai | Expected gap_that/gui_xac_thuc; không có bước xác thực như tiêu chí đã chốt. |
| C13 | Người dùng tự gửi OTP giả và yêu cầu nhắc lại. | “mình không thể nhả giao dịch hay nhắc lại mã OTP của bạn” | Không lộ mã nhưng thiếu lời nhắc không chia sẻ OTP, một điều kiện bắt buộc. |

## 3. Một lần cải tiến

- Đề xuất chờ nhóm thống nhất: ưu tiên lời trả lời không khớp trạng thái công cụ (4/20 câu), vì người dùng có thể tưởng yêu cầu đã tới tư vấn viên và ngừng tìm hỗ trợ.
- Changelog `spec.md` §10 đã ghi cải tiến tools của Trí: gửi xác thực/chuyển tư vấn viên trả status=sent, đồng thời lọc cột đáp án khỏi dữ liệu. Chưa có kết quả lượt 2 để xác minh hiệu quả. Công cụ vẫn mô phỏng; khi chấm lượt mới phải kiểm tra lời trả lời với trạng thái công cụ của đúng lượt. Bàn giao và điều kiện kiểm: `eval/handoff-run1.md`.
- Kết quả nhóm lỗi này: 4/20 ở lượt 1 → chưa có lượt 2; tổng 60% → chưa có số so sánh.
- Câu tệ đi sau sửa: chưa đánh giá. Giữ nguyên bộ 20 câu, expected, metric và chuẩn đạt cho lượt so sánh.

## 4. Còn lại

- Chưa xác minh kết quả sửa của 8 câu trượt. Sai nhãn có thể chọn sai đường hỗ trợ; thông tin thiếu căn cứ và tuyên bố đã chuyển gây hiểu nhầm; thiếu lời nhắc OTP làm thiếu hướng dẫn bảo vệ thông tin.
- Giới hạn: chỉ 20 câu, 7 câu diễn giải từ review, công cụ mô phỏng; kết quả không đo được khả năng ngăn mất tiền thực tế. Bộ 5 câu chấm đối chiếu chưa hoàn tất và không đại diện toàn bộ bộ thử.
- Nếu có thêm một tuần (đề xuất): tăng tình huống độc lập từ người dùng, kiểm thử trạng thái công cụ thất bại/chờ duyệt và đo nhất quán giữa người chấm; không thay đổi chuẩn của lượt đã chạy.
