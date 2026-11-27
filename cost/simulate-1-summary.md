# Tóm tắt mô phỏng simulate-1@20261127-230211

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| nguoi_lon_tuoi_bi_giuc | 13 | 5 | 6902 | 734 | 5.0 | 8.0 |
| chu_shop_nho_gap_that | 27 | 2 | 2761 | 292 | 2.0 | 3.2 |
| nguoi_bi_chiem_tai_khoan | 8 | 3 | 4141 | 441 | 3.0 | 5.0 |

Tỉ lệ đạt dùng để tính: 15/20 (75%) — lượt run-2@20261127-215329

- Tự chọn: lượt run-N mới nhất đã chấm xong, chạy bằng đúng model đang đo (run-2.csv). Muốn dùng lượt khác (vd lượt 2): thêm `--rate-from eval/run-2.csv`.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (30.350 người) | Chi phí / tháng — cơ sở (66.770 người) | Chi phí / tháng — cao (121.400 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0017 (≈ 44 ₫) | $0.0022 (≈ 58 ₫) | $0.00075 (≈ 20 ₫) | $98.51 (≈ 2.564.167 ₫) | $216.72 (≈ 5.641.168 ₫) | $394.03 (≈ 10.256.670 ₫) | $0.0032 (≈ 84 ₫) |
| gemini-3.8-flash (vào 1.5 · ra 7.5 $/1M) | $0.0094 (≈ 246 ₫) | $0.0126 (≈ 328 ₫) | $0.0042 (≈ 110 ₫) | $552.76 (≈ 14.388.461 ₫) | $1,216.08 (≈ 31.654.613 ₫) | $2,211.06 (≈ 57.553.842 ₫) | $0.0182 (≈ 474 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (3.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 2/50.
- Tỷ giá: 1 USD = 26.030 ₫ (https://www.vietcombank.com.vn/ (ngày 27/11/2026)).
