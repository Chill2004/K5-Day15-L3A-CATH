# Reflection — Hoàng Ngọc Minh Trí

1. Vai trò + phần mình làm (trỏ tới file / commit):

   Mình ở cặp X cùng Cường, phụ trách luồng và công cụ của bản chạy thử: `codebase/agent.py` và `codebase/tools.py`. `answer()` chạy theo luồng cố định ở `spec.md` §4: tra giao dịch → `classify` → `guard` → gọi công cụ theo `hanh_dong` → trả JSON `nhom`, `hanh_dong`, `tra_loi`, `tom_tat` để chấm (`3abece8`, `341c402`, `06f3bc0`). Trong `tools.py` có 4 công cụ `@tool` và 2 công cụ bị chặn (`release_transaction`, `lock_wallet`) chỉ trả bản nháp chờ duyệt. Cột đáp án như `nhom_that` bị lọc 2 lớp, khi đọc data và qua whitelist `_CLASSIFY_KEYS` (`cf038d2`). Cải tiến duy nhất cho lượt 2 là của mình: `handoff_to_agent` và `request_verification` trả `status=sent` (`5f89715`, `spec.md` §10). Mình cùng Ánh và Cường duyệt đáp án, metric và chuẩn đạt trước CP2. Lượt 2 (`run-2@20261127-215329`) mình chấm đối chiếu 20 câu có AI hỗ trợ (`eval/tri-review-comparison.md`).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

   Mình dùng Claude Code viết nháp `agent.py`, `tools.py` và docstring 4 ý cho từng công cụ. Mình phải tự gỡ xung đột merge giữa nhánh `hmt` và `ntc` (`1fd8672`). Mình bỏ đoạn so khớp từ khoá AI viết để luôn gọi `classify`, vì so khớp từ khoá dễ thành giấu câu thử vào code. Mình cũng thêm lớp lọc cột đáp án. Trong `tools.py` vẫn còn một đoạn code thừa AI để lại (`_strip_accents`, `_MOCK_TRANSACTIONS`, `_match_transaction`): không được gọi nên không ảnh hưởng kết quả, nhưng `_strip_accents` dùng `unicodedata` chưa import. Mình chưa dọn đoạn này. Lượt 2 mình cũng nhờ Claude Code chấm thử 20 câu: AI cho 16/20, bảng chính thức 15/20, khớp 17/20, riêng C01–C05 khớp 3/5. Trước khi chấm, AI đã đọc `eval/cuong-review-5.md` và tổng 15/20 trong `eval/report.md`, còn mình đã duyệt spec. Vì vậy bản này chỉ là **chấm đối chiếu có tham khảo, không tính là chấm độc lập**. Kiểm tra độc lập thật là phiếu của K1 trên lượt 1, khớp 4/5 (`eval/peer-review-run1.md`).

3. Một câu thử trượt của nhóm và mình học được gì từ nó:

   C03 ở lượt 1 đúng nhãn nhưng trượt: bot nói "đã chuyển yêu cầu đến tư vấn viên" trong khi `handoff_to_agent` của mình trả `status=draft`, `requires_human_approval=True`. C09, R03, R05 trượt cùng kiểu. Lượt 2, mình đổi hai công cụ có thể đảo lại sang `sent` theo `spec.md` §4, và cả bốn câu đạt lại. Bài học: lời trả lời phải khớp trạng thái công cụ, và đây vẫn chỉ là trạng thái trong mô phỏng, chưa chứng minh gửi được tới ví thật. Khi chấm lại C03 ở lượt 2, mình cho 0 vì ý "nghi truy cập trái phép" chỉ có trong `tom_tat` cho tư vấn viên, không có trong `tra_loi`; Ánh tính cả `tom_tat` nên cho 1. C05 và C07 thì ngược lại: Ánh cho trượt vì khẳng định tuyệt đối thiếu căn cứ, mình chỉ ghi giáp ranh. C13 trượt ở cả hai bảng vì thiếu lời nhắc không chia sẻ OTP. Vì `an_toan_va_tham_quyen` đòi 100% câu từ chối, lượt 2 vẫn chưa đạt. Mình học được ba điều: giữ nguyên điểm ban đầu của mỗi bên và ghi kết luận sau thảo luận riêng; không sửa metric hay điểm cho đủ ngưỡng 4/5 hoặc 80%; và ghi đúng phần AI chấm là đối chiếu có tham khảo, tách khỏi phiếu chấm độc lập.

4. Việc còn lại (trước 23:59 Thứ Bảy 28/11):

   - Đọc lại, sửa reflection này theo trải nghiệm thật rồi commit lên nhánh `hmt` để nhóm duyệt.
   - Khai thêm vào `docs/ai-usage.md` việc chấm đối chiếu lượt 2 bằng Claude Code (không độc lập) và việc AI hỗ trợ soạn nháp reflection này.
   - Thống nhất với Ánh cách hiểu C03 (`tom_tat` có tính vào pass_criterion không) và mức áp dụng metric "không bịa" cho C05, C07. Ghi kết luận sau thảo luận riêng, không sửa điểm đã chấm.
   - Nếu còn thời gian: dọn đoạn code thừa trong `tools.py` trên nhánh riêng. Không chạy lại hay sửa `run-*.csv` và `traces/`.
