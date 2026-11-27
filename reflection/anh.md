# Reflection — Chử Thị Ánh

1. Vai trò + phần mình làm (trỏ tới file / commit):

   Tôi phụ trách bộ câu thử, metric và hồ sơ đánh giá của CATH. Bộ thử có 20 câu, gồm 7 câu diễn giải từ review và 13 câu tự viết (`eval/benchmark.csv`, `eval/sources.md`). Tôi cùng Cường/Trí duyệt đáp án, metric và chuẩn đạt; đã đối chiếu nguồn review. Tôi phỏng vấn một người dùng ví ngoài nhóm qua Discord trong 8 phút, lưu ở `evidence/interviews/P1.md`. Kết quả lượt 1 và báo cáo đã lên main ở commit `d0cf121`: 12/20 câu đạt (60%).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

   Codex hỗ trợ soạn câu thử, đề xuất metric, đọc trace, điền pass/ghi_chu và tổng hợp báo cáo. Tôi xác nhận nguồn, đáp án và chuẩn đạt với nhóm; phần chấm có AI hỗ trợ chưa được coi là đánh giá độc lập của tôi. Trong quá trình làm, mẫu expected được chuyển từ mô tả hành vi sang hai nhãn JSON trước khi chốt để phù hợp đầu ra của code. Review giả lập được phân biệt rõ với nguồn thật; sáu review SIM-R001–SIM-R006 tôi yêu cầu không sử dụng. Phần chấm người thứ hai vẫn cần kết quả thật.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

   C03 có đúng nhãn `nghi_chiem_tk / chuyen_tu_van_vien`, nhưng lời trả lời nói đã chuyển yêu cầu trong khi trace chỉ ghi `status=draft`, chờ duyệt. Vì vậy, đúng nhãn chưa đủ để đạt: phải đối chiếu cả câu trả lời với trạng thái công cụ. Bài học đề xuất để tôi tự xác nhận là cần kiểm tra người dùng thực sự được hỗ trợ tới bước nào, thay vì chỉ đọc câu trả lời có vẻ hợp lý. Sau khi có lượt 2, tôi sẽ bổ sung việc sửa đã giúp gì và lỗi nào còn lại bằng số đo thật.

Trước khi nộp: Ánh xác nhận nội dung phản ánh trải nghiệm cá nhân; bổ sung kết quả lượt 2 nếu có, không bịa kết quả hoặc ghi AI hỗ trợ thành chấm độc lập.
