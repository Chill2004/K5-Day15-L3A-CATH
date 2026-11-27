# CATH · Chia việc theo từng checkpoint

**Track E3 — hỗ trợ khi giao dịch nghi lừa đảo bị tạm chặn.** Chia theo cặp như guide yêu cầu:

- **Cặp X — Cường (đội trưởng) + Trí:** phần code (khung bản chạy thử, công cụ, nối model, chặn rủi ro)
- **Cặp Y — Ánh + Hà:** phần đánh giá và data (câu thử, metric, data giả, chi phí)

Ai cũng phải giải thích được phần có tên mình và chạy được `python run.py eval` / `python run.py simulate`. Giám khảo hỏi bất kỳ ai.

---

## CP1 — 17:00 Thứ Sáu 27/11

| Người | Việc |
|---|---|
| Cả nhóm | Đọc tóm tắt hướng E3, chốt hướng và phân công này |
| Cường | Commit, push, mở repo bằng cửa sổ ẩn danh để kiểm, nộp form CP1 |

---

## CP2 — 19:30 Thứ Sáu 27/11

| Người | Việc | File |
|---|---|---|
| Cường | Ghi trước cách chọn mẫu review và định nghĩa từng nhãn (trước khi gắn nhãn) · lấy API key, gọi thử được 1 câu | `evidence/data-mining.md` |
| Trí | Khung bản chạy thử chạy hết luồng với AI giả (`python run.py`) · công cụ trả data giả · vẽ sơ đồ luồng | `codebase/agent.py`, `codebase/tools.py`, `spec.md` §4 |
| Ánh | ≥10 câu thử (≥1/3 câu dựa trên review thật hoặc lời phỏng vấn) · ≥3 metric (định nghĩa, cách chấm, ngưỡng) · xoá 3 câu mẫu B01–B03 | `eval/benchmark.csv`, `eval/metric_spec.yaml` |
| Hà | Dựng data giả: giao dịch bị giữ, tin nhắn mẫu (có seed, nhãn `synthetic`) · data card bản đầu | `data/`, `data/DATA_CARD.md` |
| Cả nhóm | **Chốt chuẩn "đạt" bằng số — sau mốc này không được sửa** · cập nhật canvas dòng "đã đổi gì so với CP1" · mỗi người hẹn ≥1 người để phỏng vấn | `spec.md` §7, `canvas.md` |

Kiểm trước khi nộp: `python run.py check` không còn cảnh báo về câu thử và metric.

---

## Tối Thứ Sáu → CP3 — 10:00 Thứ Bảy 28/11

| Người | Việc | File |
|---|---|---|
| Cường | Nối model thật (key để trong `.env`, **không commit**), chạy `python run.py eval --try` thấy token > 0 · cài chỗ chặn rủi ro: code chặn mọi lệnh nhả giao dịch / khoá ví gọi từ AI · gắn nhãn tay review, đếm x/N, chọn ≥5 trích dẫn | `codebase/ai.py`, `evidence/data-mining.md`, `evidence/summary.md` |
| Trí | Hoàn thiện công cụ, ghép với model thật · viết README phần lệnh chạy | `codebase/agent.py`, `codebase/tools.py` |
| Ánh | Mở rộng lên 20–30 câu thử: ≥5 câu `kho`, ≥2 câu `tu_choi` gồm 2 câu tấn công (dò ngưỡng, giả nhân viên ngân hàng) | `eval/benchmark.csv` |
| Hà | Viết thêm tin nhắn mẫu cho câu thử mới · cập nhật data card · nháp persona chi phí | `data/`, `data/DATA_CARD.md`, `cost/personas.yaml` |
| Mỗi người | Phỏng vấn ≥1 người dùng ví ngoài nhóm (10–15 phút, hỏi chuyện 1 tháng qua, không hỏi số tiền, số tài khoản) | `evidence/interviews/P1.md`… |
| Cả nhóm (sáng T7) | Chạy lượt 1 cùng nhau, chấm cột `pass`, `python run.py score` · quay video 30 giây (AI trả kết quả thật) | `eval/run-1.csv` |

---

## CP4 — 14:30 Thứ Bảy 28/11

| Người | Việc | File |
|---|---|---|
| Cả nhóm | Ngồi chung đọc các câu trượt của lượt 1, gom thành nhóm lỗi, chọn **1** nhóm lỗi đau nhất để sửa | — |
| Cường + Trí | Sửa theo nhóm lỗi đã chọn, chạy lượt 2 trên **cùng bộ câu thử** | `eval/run-2.csv` |
| Ánh | Báo cáo đánh giá: % lượt 1 → lượt 2, ≥3 lỗi (input · output · vì sao sai) · hồ sơ đánh giá một trang | `eval/report.md`, `eval/README.md` |
| Hà | Mô phỏng chi phí: ≥3 persona, `python run.py simulate` ≥50 phiên, 3 kịch bản thấp · cơ sở · cao, ≥2 mức model, cộng giờ công tư vấn viên | `cost/personas.yaml`, `cost/cost-estimate.md` |
| Một cặp | Slide 8 trang (mỗi trang ≥1 con số có nguồn) | slide trong repo hoặc link |
| Cặp còn lại | Quay video demo dự phòng | link video |
| Cường | Nộp form CP4 | — |

---

## Hạn chót — 23:59 Thứ Bảy 28/11

| Người | Việc |
|---|---|
| Mỗi người | 1 file `reflection/<ten-khong-dau>.md`: phần mình làm · AI hỗ trợ thế nào · 1 bài học từ 1 câu thử trượt |
| Cả nhóm | Mọi thay đổi sau 14:30 ghi vào `spec.md` §10 |

---

## Không được làm (bị trừ điểm nặng)

- Commit API key hoặc dữ liệu cá nhân thật → −10 điểm
- Sửa chuẩn "đạt" sau CP2, xoá câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy → phần đó 0 điểm
- Dùng người trong nhóm, data tự tạo hoặc chat với AI làm bằng chứng pain
