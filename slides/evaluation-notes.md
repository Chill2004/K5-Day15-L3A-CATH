# Nội dung chuẩn bị cho slide 5 — Đánh giá thế nào

Trạng thái: nội dung dự thảo để ghép vào slide chung, chưa phải bộ slide hoàn chỉnh. Chưa có số lượt 2 hoặc độ khớp người chấm.

## Nội dung đưa lên slide

- Bộ thử: **20 câu** — 5 thường, 12 khó, 3 từ chối; **7/20** từ review, 13 tự viết. Nguồn: `eval/benchmark.csv`, `eval/sources.md`.
- Chấm cả nhãn, hành động và nội dung; kiểm lời trả lời bằng trace công cụ. Metric và chuẩn đạt giữ nguyên sau CP2. Nguồn: `eval/metric_spec.yaml`, `spec.md` §7.
- Lượt 1: **12/20 đạt (60%)** — thường 3/5, khó 7/12, từ chối 2/3. **Chưa đạt chuẩn** ≥80% tổng và 100% câu từ chối. Nguồn: `python run.py score eval/run-1.csv`.
- Hai nhãn đúng ở **18/20 câu**, nhưng không thay thế pass tổng. Nhóm lỗi lớn nhất: **4/20 câu** nói đã chuyển yêu cầu dù công cụ mới tạo nháp. Nguồn: output, ghi_chu và trace lượt 1.
- Run ID: `run-1@20261127-184833`; model: `gemini-3.1-flash-lite`. Công cụ mô phỏng; chưa đo được tác động ngăn mất tiền thực tế.
- Lượt 2: **chưa có kết quả**, sẽ so trên cùng bộ câu thử. Không điền số ước đoán.

## Lời nói dự thảo khoảng 45 giây

Nhóm đánh giá trên 20 câu, trong đó 7 câu dựa trên review có nguồn. Một câu chỉ đạt khi đúng nhãn, đúng hành động và đáp ứng tiêu chí nội dung, an toàn. Lượt 1 đạt 12 trên 20 câu, tức 60%, chưa đạt chuẩn nhóm chốt. Dù hai nhãn đúng ở 18 câu, một số câu vẫn trượt vì lời trả lời nói đã chuyển yêu cầu trong khi công cụ mới tạo bản nháp. Nhóm lỗi này xuất hiện ở bốn câu và được chọn làm mục tiêu cải tiến theo changelog của nhóm. Kết quả chấm có AI hỗ trợ; đối chiếu người thứ hai và kết quả lượt 2 chưa hoàn tất.

## Chuẩn bị cho câu hỏi của giám khảo

- Vì sao 90% đúng nhãn mà chỉ 60% đạt? Câu còn phải qua điều kiện nội dung và metric; C03 là ví dụ lời trả lời không khớp trạng thái công cụ.
- Nguồn thật có đại diện mọi người dùng không? Không; review nghiêng về phàn nàn, một số tình huống rộng hơn lát cắt giữ vì nghi rủi ro.
- Đã giảm mất tiền thật chưa? Chưa đo; chỉ đánh giá bản chạy thử với công cụ mô phỏng.
- Đã chứng minh cải tiến hiệu quả chưa? Chưa có lượt 2; không kết luận hiệu quả từ thay đổi code.
