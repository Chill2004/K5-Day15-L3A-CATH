# Giả thuyết — viết TRƯỚC khi tìm bằng chứng (5 phút, commit ngay)

> Điền ở guide bước 1.1. Ôn lại: ngày 2 · lab ngày 2.
> Viết **trước** khi đọc dòng data đầu tiên hay hỏi người đầu tiên, để không sửa cho khớp kết quả. Kết quả ngược giả thuyết vẫn đủ điểm nếu số là thật.

- Ngày giờ viết: 12:23 27/11/2026
- **Khai thật về thứ tự:** trước khi viết file này, nhóm đã xem số đếm thử bằng từ khoá (review Google Play VN và Mỹ/Anh, số đếm theo nhãn của CFPB) để chọn hướng trong Track E. Số đếm thử đó chỉ dùng để chọn hướng, **không** dùng làm bằng chứng chính thức. Bằng chứng chính thức là một mẫu ngẫu nhiên có seed, gắn nhãn tay theo định nghĩa nhãn ghi trước ở `evidence/data-mining.md` (lần đếm thử chỉ lọc bằng từ khoá, chưa đọc và gắn nhãn từng review).
- Người dùng chính (một vai cụ thể): người dùng ví điện tử vừa có giao dịch chuyển tiền bị ví tạm giữ vì nghi rủi ro, đang nhắn vào chat hỗ trợ ngoài giờ nhân viên trực hoặc lúc nhân viên quá tải.
- **Mình nghĩ:** người dùng ví gặp khó khi giao dịch bị tạm giữ vì kênh hỗ trợ trả lời chậm hoặc chung chung, không phân biệt được người đang bị kẻ gian giục chuyển với người gấp thật; hậu quả là người bị lừa vẫn chuyển được tiền đi, còn người gấp thật mất thời gian và mất lòng tin vào ví.
- **Có thể còn cách giải thích khác:** người dùng bực vì bị khoá hay giữ tiền nói chung (thủ tục xác thực, lỗi app), không phải vì bị lừa; hoặc giao dịch bị giữ rất hiếm ở Việt Nam, nên pain chủ yếu nằm ở thị trường khác.
- **Mình đúng nếu thấy:**
  - Trong mẫu review 1–2 sao gắn nhãn tay, **≥10%** thuộc nhãn "tài khoản / giao dịch bị khoá, giữ" hoặc "lừa đảo, giao dịch trái phép"; và
  - **≥2/3 người** được phỏng vấn kể được một lần cụ thể trong 1 tháng qua họ hoặc người thân bị giữ giao dịch, hoặc nhận cuộc gọi / tin nhắn giục chuyển tiền gấp.
- **Nguồn sẽ dùng** (≥1 nguồn đạt ngưỡng, guide 1.2): [x] đào data · [x] phỏng vấn ≥3 · [ ] khảo sát ≥20 — nguồn chính: đào data (CFPB Consumer Complaint Database, khiếu nại nhận từ 27/11/2025 đến 27/11/2026, kèm số cả năm 2025 để đối chiếu + review Google Play của ví/ngân hàng VN, Mỹ, Anh; mentor đã xác nhận được dùng data nhiều nước) · nguồn để kiểm lại: phỏng vấn ≥3 người dùng ví ở Việt Nam, ngoài nhóm.
