# Phiếu chấm người thứ hai — lượt 1

## Cập nhật phiếu đã nhận ngày 28/11/2026

Theo yêu cầu Ánh, `eval/review-5-blind.csv` hiện lưu điểm và ghi chú Trí gửi cho C01–C05: 1, 1, 0, 1, 1. Nhận xét được đối chiếu với lượt `run-2@20261127-215329`, nên phiếu dùng đúng output và tool_results lượt 2; chưa có xác nhận run ID riêng từ Trí. Phiếu trống lượt 1 ban đầu được giữ ở `eval/review-5-run1-blank.csv`. Không thay đổi bất kỳ file run hoặc trace nào.

Điểm Trí khớp 3/5 với điểm hiện tại của cùng lượt 2; lệch C03, C05. Đây là số đối chiếu thực tế, chưa đủ 4/5. Chưa xác nhận điều kiện độc lập, không ghi là đã đạt yêu cầu kiểm chấm độc lập. Hướng dẫn lượt 1 bên dưới giữ làm lịch sử quy trình, không mô tả phiếu hiện tại.

## Gói gửi người chấm

Gửi `eval/review-5-blind.csv`, file hướng dẫn này và `eval/metric_spec.yaml`. Phiếu dùng C01–C05 từ cùng lượt `run-1@20261127-184833`, kèm kết quả công cụ của chính lượt đó. Không có pass và ghi_chu đã chấm trong phiếu. Không gửi run-1.csv hoặc report.md trước khi nhận lại điểm.

Chọn người không viết spec và chưa xem điểm/lý do chấm các output của lượt này. Cường đã tham gia duyệt chuẩn và đã xem đánh giá trước đó, nên cần kiểm tra điều kiện này; nếu không đáp ứng, nhờ thành viên khác đủ điều kiện. Nếu không tìm được, ghi đúng là đối chiếu có tham khảo, không báo là chấm độc lập.

## Tin nhắn nhờ chấm

> Bạn ơi, mình nhờ bạn chấm 5 output C01–C05 của lượt run-1@20261127-184833 theo metric nhóm đã chốt. Phiếu có input, expected, output, tiêu chí và kết quả công cụ; chưa có điểm của lượt chấm trước. Bạn giúp điền pass_nguoi_2 bằng 1/0 và ghi_chu_nguoi_2 nêu lý do, không sửa cột khác. Bạn đã tham gia viết spec hoặc xem điểm/lý do chấm của đúng các output này chưa? Nếu chưa, bạn dành khoảng 15–20 phút chấm rồi gửi lại giúp mình nhé. Chưa trao đổi đáp án chấm trước khi gửi phiếu.

## Cách chấm

- Đọc nguyên metric đã chốt, không đổi tiêu chí hoặc ngưỡng.
- Hai nhãn phải khớp expected. Nội dung phải đáp ứng toàn bộ pass_criterion và ba metric ở cấp câu như quy tắc trong hồ sơ đánh giá.
- Đối chiếu lời tuyên bố thao tác với tool_results; phân biệt bản nháp và kết quả thực hiện. Không mặc định có gọi tool là đã gửi/đã chuyển thành công.
- Điền 1 khi đạt đủ; 0 khi có điều kiện không đạt, ghi bằng chứng cụ thể. Không dùng điểm 10/10. Đánh dấu điểm cần thảo luận trong ghi chú nhưng vẫn đưa quyết định chấm ban đầu.
- Chỉ chấm output của lượt chỉ định, không chạy lại model. Tránh xem file chứa điểm lượt trước cho đến khi gửi phiếu.

## Đối chiếu sau khi nhận phiếu

1. Giữ nguyên bản phiếu ban đầu và danh tính người chấm theo vai/tên thành viên, thời điểm, xác nhận không xem điểm trước.
2. So 5 giá trị pass_nguoi_2 với pass tương ứng trong run-1.csv; số khớp là số cặp bằng nhau, mẫu số luôn 5.
3. Ghi các câu lệch và lý do; phân biệt kết quả trước thảo luận với kết luận sau thảo luận. Không sửa output/expected, metric hoặc chuẩn đạt.
4. Điền độ khớp thật vào eval/README.md. Nếu dưới 4/5, ghi hạn chế và trao đổi cách áp dụng tiêu chí; sau CP2 không viết lại metric để làm khớp điểm.

## Trạng thái

- Người chấm thứ hai: Trí, theo bảng Ánh chuyển tiếp; chưa xác nhận điều kiện độc lập.
- Đã nhận kết quả: Ánh đã chuyển bảng 20 câu; đã nhập 5 câu đầu vào phiếu theo yêu cầu. Codex chưa gửi tin ra ngoài.
- Độ khớp C01–C05 cùng lượt 2: 3/5; chưa có kết luận đồng thuận cho các câu lệch.
- Lượt chấm ban đầu trong run-1.csv có AI hỗ trợ, không mô tả là Ánh chấm độc lập.
