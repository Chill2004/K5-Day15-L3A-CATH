# CATH · Chia việc theo checkpoint (Track E3)

| Cặp | Thành viên | Phần chính |
|---|---|---|
| **X** | Nguyễn Thế Cường (đội trưởng) + Hoàng Ngọc Minh Trí | Code: khung chạy thử, công cụ, nối model, chặn rủi ro |
| **Y** | Chử Thị Ánh + Nguyễn Thị Thu Hà | Đánh giá và data: câu thử, metric, data giả, chi phí |

Ai cũng phải giải thích được phần có tên mình và chạy được `python run.py eval` / `python run.py simulate`. Phân công này khớp với `TEAMS.md` và `canvas.md` dòng 7 — đổi người thì sửa cả ba file.

## CP1 · 17:00 Thứ Sáu 27/11

| Người | Việc |
|---|---|
| Cả nhóm | Đọc tóm tắt E3, chốt hướng |
| Cường | Nộp form CP1 |

## CP2 · 19:30 Thứ Sáu 27/11

| Người | Việc | File |
|---|---|---|
| Cường | Ghi trước cách chọn mẫu và nhãn review *(đã xong, nhánh `ntc`)* · lấy API key, gọi thử được 1 câu | `evidence/data-mining.md` |
| Trí | Khung bản chạy thử chạy hết luồng với AI giả · sơ đồ luồng | `codebase/agent.py`, `codebase/tools.py`, `spec.md` §4 |
| Ánh | ≥10 câu thử (≥1/3 dựa trên review thật hoặc lời phỏng vấn) · ≥3 metric · xoá câu mẫu B01–B03 | `eval/benchmark.csv`, `eval/metric_spec.yaml` |
| Hà | Dựng data giả (giao dịch bị giữ, tin nhắn mẫu, có seed, nhãn `synthetic`) · data card bản đầu | `data/`, `data/DATA_CARD.md` |
| Cả nhóm | **Chốt chuẩn "đạt" — sau mốc này không sửa nữa** · cập nhật canvas dòng "đã đổi gì so với CP1" · mỗi người hẹn ≥1 người để phỏng vấn | `spec.md` §7, `canvas.md` |

## Tối T6 → CP3 · 10:00 Thứ Bảy 28/11

| Người | Việc | File |
|---|---|---|
| Cường | Nối model thật (key trong `.env`, **không commit**) · chặn mọi lệnh nhả giao dịch / khoá ví gọi từ AI · kiểm lại 400 nhãn review, chọn ≥5 trích dẫn | `codebase/ai.py`, `evidence/` |
| Trí | Hoàn thiện công cụ, ghép với model thật · phần lệnh chạy trong README | `codebase/agent.py`, `codebase/tools.py` |
| Ánh | Mở rộng 20–30 câu thử: ≥5 câu `kho`, ≥2 câu `tu_choi` (gồm 2 câu tấn công) | `eval/benchmark.csv` |
| Hà | Gắn nhãn 40 review kiểm chéo (không xem nhãn khác) · viết thêm tin nhắn mẫu · nháp persona chi phí | `evidence/reviews_check_ha.csv`, `data/`, `cost/personas.yaml` |
| Mỗi người | Phỏng vấn ≥1 người dùng ví ngoài nhóm (10–15 phút, chuyện 1 tháng qua, không hỏi số tiền / số tài khoản) | `evidence/interviews/P1.md`… |
| Cả nhóm (sáng T7) | Chạy lượt 1 · chấm cột `pass` · quay video 30 giây | `eval/run-1.csv` |

## CP4 · 14:30 Thứ Bảy 28/11

| Người | Việc | File |
|---|---|---|
| Cả nhóm | Đọc các câu trượt, chọn 1 nhóm lỗi để sửa | — |
| Cường + Trí | Sửa, chạy lượt 2 trên cùng bộ câu thử | `eval/run-2.csv` |
| Ánh | Báo cáo đánh giá: % lượt 1 → lượt 2, ≥3 lỗi (input · output · vì sao sai) | `eval/report.md`, `eval/README.md` |
| Hà | Mô phỏng chi phí: ≥3 persona, ≥50 phiên, 3 kịch bản, ≥2 mức model, cộng giờ công tư vấn viên | `cost/` |
| Một cặp | Slide 8 trang (mỗi trang ≥1 con số có nguồn) | slide |
| Cặp còn lại | Video demo dự phòng | link video |
| Cường | Nộp form CP4 | — |

## Hạn chót · 23:59 Thứ Bảy 28/11

| Người | Việc |
|---|---|
| Mỗi người | 1 file `reflection/<ten-khong-dau>.md` |
| Cả nhóm | Mọi thay đổi sau 14:30 ghi vào `spec.md` §10 |

## ⚠️ Không được làm

| Lỗi | Hậu quả |
|---|---|
| Commit API key | −10 điểm |
| Sửa chuẩn "đạt" sau CP2, xoá câu thử trượt, sửa `expected` cho khớp kết quả | Phần đó 0 điểm |
| Dùng người trong nhóm, data tự tạo hoặc chat với AI làm bằng chứng | Không tính là bằng chứng |
