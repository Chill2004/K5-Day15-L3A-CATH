# Data card — dữ liệu bản chạy thử dùng

> Bản đầu CP2 (27/11/2026). Người viết: Nguyễn Thị Thu Hà. Chấm ở rubric R4.
> Không commit dữ liệu cá nhân thật hay nguyên file data BTC cấp.

## Dataset 1 · Giao dịch bị tạm giữ (`data/held_transactions.csv`)

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ tra giao dịch bị giữ (`codebase/tools.py`) · ngữ cảnh khi chạy `eval` / `simulate` |
| Từ đâu | sinh có seed bằng `data/gen_synthetic.py` (nhóm tự viết) |
| Xử lý những bước gì | không có data thật nên không cần ẩn danh · mã người dùng `U001…`, mã giao dịch `TX0001…` đều bịa |
| Số dòng / số đoạn | 30 giao dịch |
| Phiên bản / ngày lấy | v1 · sinh ngày 27/11/2026 · seed 42 |
| Nhãn | `synthetic` (cột `nhan`) |
| Giới hạn | số tiền, lý do giữ, kênh chọn ngẫu nhiên, không phản ánh phân bố thật của ví nào · cột `nhom_that` là đáp án, agent không được đọc · không có ngưỡng phát hiện gian lận (ngưỡng nằm trong code) |

## Dataset 2 · Tin nhắn mẫu của người dùng (`data/messages.csv`)

| | |
|---|---|
| Dùng để làm gì | tin nhắn mẫu cho 4 nhóm phân loại (`bi_giuc`, `gap_that`, `chiem_tk`, `chua_ro`) · thử nhanh bản chạy thử |
| Từ đâu | nhóm tự viết (17 câu gốc trong `gen_synthetic.py`), lấy ý từ các kiểu phàn nàn đọc được ở review Google Play (`evidence/data-mining.md` §2), không chép nguyên văn review |
| Xử lý những bước gì | mỗi giao dịch ghép 1 tin nhắn cùng nhóm, chọn ngẫu nhiên theo seed |
| Số dòng / số đoạn | 30 tin nhắn (bi_giuc 9 · gap_that 8 · chiem_tk 7 · chua_ro 6) |
| Phiên bản / ngày lấy | v1 · 27/11/2026 · seed 42 |
| Nhãn | `synthetic` · `nguon = tu_viet` |
| Giới hạn | câu do người trong nhóm viết nên gọn và rõ hơn tin nhắn thật lúc đang hoảng (ít lỗi chính tả, ít viết tắt) · lệch về kịch bản lừa đảo phổ biến ở VN · **không phải bằng chứng pain** và không tính vào ≥1/3 câu thử từ người dùng / data thật |

**Data `synthetic`:** cách sinh `python data/gen_synthetic.py` · seed 42 · người kiểm: Nguyễn Thị Thu Hà · số dòng đã kiểm tay: __/30 (đọc từng tin nhắn, xác nhận `nhom_that` đúng).

## Dataset 3 · Review Google Play đã gắn nhãn (`evidence/reviews_labeled.csv`)

Xem `evidence/data-mining.md` (Cường phụ trách). Dùng để đào bằng chứng và lấy ý cho câu thử, không đưa vào công cụ của agent.
