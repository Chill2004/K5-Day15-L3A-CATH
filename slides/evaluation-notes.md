# Nội dung chuẩn bị cho slide 5 — Đánh giá thế nào

Trạng thái: nội dung để ghép vào slide chung, đã cập nhật hai lượt. Đối chiếu với Trí có AI hỗ trợ đã có số liệu; K1 đã kiểm độc lập 5 output lượt 1, khớp 4/5, đạt mốc yêu cầu. Đây chưa phải bộ slide hoàn chỉnh.

## Nội dung đưa lên slide

- Bộ thử: **20 câu** — 5 thường, 12 khó, 3 từ chối; **7/20** từ review, 13 tự viết. Nguồn: `eval/benchmark.csv`, `eval/sources.md`.
- Chấm cả nhãn, hành động và nội dung; kiểm lời trả lời bằng trace công cụ. Metric và chuẩn đạt giữ nguyên sau CP2. Nguồn: `eval/metric_spec.yaml`, `spec.md` §7.
- Lượt 1: **12/20 đạt (60%)** — thường 3/5, khó 7/12, từ chối 2/3. **Chưa đạt chuẩn** ≥80% tổng và 100% câu từ chối. Nguồn: `python run.py score eval/run-1.csv`.
- Hai nhãn đúng ở **18/20 câu**, nhưng không thay thế pass tổng. Nhóm lỗi lớn nhất: **4/20 câu** nói đã chuyển yêu cầu dù công cụ mới tạo nháp. Nguồn: output, ghi_chu và trace lượt 1.
- Run ID: `run-1@20261127-184833`; model: `gemini-3.1-flash-lite`. Công cụ mô phỏng; chưa đo được tác động ngăn mất tiền thực tế.
- Lượt 2: **15/20 đạt (75%)** — thường 4/5, khó 9/12, từ chối 2/3. Run ID: `run-2@20261127-215329`, cùng model và bộ câu thử. Nguồn: `python run.py score eval/run-2.csv`.
- So sánh: **60% → 75%, tăng 15 điểm phần trăm**. Bốn câu C03, C09, R03, R05 đạt lại; C07 từ đạt thành trượt. Hai lượt vẫn chưa đạt chuẩn tổng ≥80% và 100% câu từ chối. Nguồn: `eval/report.md`, hai file run và trace.
- Đối chiếu bảng Trí chấm có AI hỗ trợ: **17/20 khớp**, riêng C01–C05 **3/5**; lệch C03, C05, C07. Không coi là kiểm tra độc lập đạt ≥4/5. Nguồn: `eval/tri-review-comparison.md`.

- Kiểm tra chấm độc lập: **K1 khớp 4/5** trên C01–C05 lượt 1, đạt mốc ≥4/5; người chấm không viết spec/metric và chưa xem điểm trước, theo xác nhận của Ánh. Nguồn: `eval/peer-review-run1.md`.

## Lời nói dự thảo khoảng 45 giây

Nhóm đánh giá trên 20 câu, trong đó 7 câu dựa trên review có nguồn. Một câu chỉ đạt khi đúng nhãn, đúng hành động và đáp ứng tiêu chí nội dung, an toàn. Lượt 1 đạt 60%. Sau cải tiến, lượt 2 đạt 75%, tăng 15 điểm phần trăm: bốn câu lỗi trạng thái công cụ đạt lại, nhưng C07 trượt mới do khẳng định thiếu căn cứ. Nhóm vẫn chưa đạt chuẩn 80% tổng và 100% câu từ chối. Cả hai lượt giữ cùng bộ câu thử và metric. Phần chấm có AI hỗ trợ; người chấm K1 kiểm độc lập năm output lượt 1, khớp bốn trên năm, đạt mốc yêu cầu. Đối chiếu riêng với bảng Trí lượt 2 khớp 17 trên 20 câu. Đây là kết quả bản chạy thử với công cụ mô phỏng, chưa chứng minh giảm mất tiền thực tế.

## Chuẩn bị cho câu hỏi của giám khảo

- Vì sao 90% đúng nhãn mà chỉ 60% đạt? Câu còn phải qua điều kiện nội dung và metric; C03 là ví dụ lời trả lời không khớp trạng thái công cụ.
- Nguồn thật có đại diện mọi người dùng không? Không; review nghiêng về phàn nàn, một số tình huống rộng hơn lát cắt giữ vì nghi rủi ro.
- Đã giảm mất tiền thật chưa? Chưa đo; chỉ đánh giá bản chạy thử với công cụ mô phỏng.
- Đã thấy cải thiện chưa? Trên bộ cố định, pass tăng 12/20 → 15/20; bốn câu mục tiêu đạt lại nhưng một câu khác trượt mới. Không quy toàn bộ tăng trưởng cho một sửa code vì nội dung model sinh cũng thay đổi và nhóm có thêm thay đổi lọc dữ liệu.
- Vì sao chưa đạt khi lượt 2 được 75%? Chuẩn tổng là ≥80%, câu từ chối phải đạt 100%; hiện chỉ 2/3 câu từ chối đạt.
- Người thứ hai đã chấm chưa? K1 đã kiểm độc lập C01–C05 lượt 1, khớp 4/5, đạt mốc yêu cầu; C05 vẫn bất đồng, không sửa điểm. Bảng Trí có AI hỗ trợ là đối chiếu khác của lượt 2, khớp 17/20.

