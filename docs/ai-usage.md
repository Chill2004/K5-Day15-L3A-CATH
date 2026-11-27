# Ghi nhận sử dụng AI (AI Usage Log)

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử — phần model (`codebase/ai.py`, `decide.py`, `guard.py`, `thu_kho.py`, `eval/so_nhan.py`) | Claude Code | Viết nháp phần gọi Gemini REST (token lấy từ `usageMetadata`, cộng cả token suy nghĩ; tự thử lại khi lỗi 429/500/503 và lỗi mạng) · hàm `classify` gọi model 1 lần với `responseSchema` để ép ra JSON · `guard` kiểm bằng code (chặn xin OTP, lộ ngưỡng, hứa nhả, link/QR, hứa khoá ví thay tư vấn viên; tự thêm 3 ý bắt buộc khi giữ và cảnh báo) · 12 ca khó/tấn công trong `thu_kho.py` · script so nhãn với `expected` | Cường chọn model và mức giá, chạy `decide.py`, `guard.py`, `thu_kho.py` trên model thật, đọc lỗi và yêu cầu sửa đến khi qua 12/12 ca · thêm thử lại khi lỗi mạng sau khi C05 bị lỗi TimeoutError · kiểm `release_transaction` và `lock_wallet` chỉ tạo bản nháp chờ duyệt · `so_nhan.py` chỉ đọc file, không ghi vào `run-*.csv` | Nguyễn Thế Cường |
| Code bản chạy thử — luồng và công cụ (`codebase/agent.py`, `tools.py`) | __ | __ | __ | Hoàng Ngọc Minh Trí |
| Prompt / thiết kế lời gọi mô hình (`SYSTEM` trong `codebase/decide.py`) | Claude Code | Soạn nháp prompt tiếng Việt: định nghĩa 4 nhóm, cách chọn hành động theo nhóm, 9 luật cứng (không nhả, khoá hay hoàn tiền; không xin OTP; không lộ ngưỡng; phân vân thì chọn `bi_giuc_chuyen`; không gửi link; không hứa việc của tư vấn viên…) | Cường duyệt định nghĩa nhóm cho khớp nhãn đào data và đáp án bộ câu thử · lỗi tìm được qua ca khó thì sửa luật, không so khớp nguyên văn câu thử · sau lượt 1 không sửa prompt, để lượt 2 chỉ đo đúng một cải tiến (công cụ trả `sent`, của Trí) | Nguyễn Thế Cường |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code | Viết script lấy review Google Play, chọn mẫu, đếm CFPB và đếm nhãn (`evidence/scripts/`) · gắn nhãn nháp 400 review theo định nghĩa nhãn nhóm ghi trước, ca khó ghi lý do ở `ghi_chu` | Cường đọc lại 400/400 dòng, làm rõ 3 quy tắc ranh giới, sửa 2/400 dòng (stt 308, 384) · một thành viên gắn độc lập 40 review không nhìn nhãn nháp, khớp __/40 | Nguyễn Thế Cường |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Sinh data `synthetic` (nếu có) |Claude |hỗ trợ khung script gen_synthetic.py |Hà viết lại, chỉnh sửa 30 tin nhắn cho sát thực tế VN Seed 42 · kiểm tay 30 dòng | Nguyễn Thị Thu Hà |
| Viết câu thử (benchmark) | Codex | Soạn 12 câu tự viết, diễn giải/dịch 6 review đã có; đề xuất metric, chuẩn đạt và hồ sơ nguồn | Ánh đối chiếu nhãn 6 review; Ánh cùng Cường/Trí duyệt đáp án, metric và chuẩn đạt. Mỗi câu có source; không dùng 6 review giả lập SIM-R001–SIM-R006 | Chử Thị Ánh |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
