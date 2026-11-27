# Reflection — Chử Thị Ánh

1. Vai trò + phần mình làm (trỏ tới file / commit):

   Tôi phụ trách bộ câu thử, metric và hồ sơ đánh giá của CATH. Bộ thử có 20 câu, gồm 7 câu diễn giải từ review và 13 câu tự viết (`eval/benchmark.csv`, `eval/sources.md`). Tôi cùng Cường/Trí duyệt đáp án, metric và chuẩn đạt; đã đối chiếu nguồn review. Tôi phỏng vấn một người dùng ví ngoài nhóm qua Discord trong 8 phút, lưu ở `evidence/interviews/P1.md`. Tôi tổng hợp hai lượt trong `eval/report.md`: lượt 1 đạt 12/20 (60%), lượt 2 đạt 15/20 (75%), tăng 15 điểm phần trăm nhưng vẫn chưa đạt chuẩn.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

   Codex hỗ trợ soạn câu thử, đề xuất metric, đọc trace, điền pass/ghi_chu và tổng hợp báo cáo. Tôi xác nhận nguồn, đáp án và chuẩn đạt với nhóm; không coi phần AI hỗ trợ là đánh giá độc lập của mình. Trước khi chốt, expected được chuyển từ mô tả hành vi sang hai nhãn JSON phù hợp đầu ra của code. Tôi yêu cầu không sử dụng sáu review giả lập SIM-R001–SIM-R006 làm nguồn thật. Bảng Trí chấm có AI hỗ trợ đã được đối chiếu với bảng lượt 2: khớp 17/20, riêng năm câu đầu khớp 3/5; chưa có đủ xác nhận để coi là kiểm tra độc lập đạt yêu cầu.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

   Ở lượt 1, C03 đúng nhãn `nghi_chiem_tk / chuyen_tu_van_vien` nhưng lời trả lời nói đã chuyển yêu cầu trong khi trace chỉ ghi `status=draft`, chờ duyệt. Tôi rút ra rằng đúng nhãn chưa đủ: phải kiểm tra lời trả lời có phản ánh đúng trạng thái công cụ hay không. Lượt 2, bốn câu C03, C09, R03, R05 đạt lại khi công cụ trả `sent` trong mô phỏng và C09 thêm bước bảo vệ tài khoản. Tuy nhiên, C07 trượt mới do khẳng định thiếu căn cứ, nên tổng chỉ tăng từ 60% lên 75%. Tôi cần giữ nguyên tiêu chí, ghi cả cải thiện lẫn lỗi mới và không suy kết quả mô phỏng thành hiệu quả bảo vệ tiền thật.
