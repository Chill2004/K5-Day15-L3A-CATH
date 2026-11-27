# Ghi nhận sử dụng AI (AI Usage Log)

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code | Viết script lấy review Google Play, chọn mẫu, đếm CFPB và đếm nhãn (`evidence/scripts/`) · gắn nhãn nháp 400 review theo định nghĩa nhãn nhóm ghi trước, ca khó ghi lý do ở `ghi_chu` | Cường đọc lại 400/400 dòng, làm rõ 3 quy tắc ranh giới, sửa 2/400 dòng (stt 308, 384) · một thành viên gắn độc lập 40 review không nhìn nhãn nháp, khớp __/40 | Nguyễn Thế Cường |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Sinh data `synthetic` (nếu có) |Claude |hỗ trợ khung script gen_synthetic.py |Hà viết lại, chỉnh sửa 30 tin nhắn cho sát thực tế VN Seed 42 · kiểm tay 30 dòng | Nguyễn Thị Thu Hà |
| Viết câu thử (benchmark) | Codex | Soạn 12 câu tự viết, diễn giải/dịch 6 review đã có; đề xuất metric, chuẩn đạt và hồ sơ nguồn | Ánh đối chiếu nhãn 6 review; Ánh cùng Cường/Trí duyệt đáp án, metric và chuẩn đạt. Mỗi câu có source; không dùng 6 review giả lập SIM-R001–SIM-R006 | Chử Thị Ánh |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
