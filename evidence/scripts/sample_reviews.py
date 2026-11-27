"""Chọn mẫu ngẫu nhiên (có seed) từ review thô → bảng để gắn nhãn tay.

Cách chọn mẫu (ghi trước khi gắn nhãn, xem evidence/data-mining.md):
  - Chỉ lấy review 1–2 sao, nội dung dài hơn 20 ký tự (bỏ "tệ", "ok"…)
  - Lấy ngẫu nhiên SAMPLE_PER_MARKET review mỗi nhóm thị trường (VN; US+UK), seed cố định
  - Mỗi review chỉ trích tối đa 2 câu (luật dùng dữ liệu)

Chạy:  python evidence/scripts/sample_reviews.py
Vào:   evidence/raw/reviews_raw.csv
Ra:    evidence/reviews_labeled.csv  (commit file này; người gắn nhãn điền cột nhan_*)
"""
import csv
import os
import random
import re

SEED = 42
SAMPLE_PER_MARKET = 200
MIN_LEN = 20
IN = os.path.join("evidence", "raw", "reviews_raw.csv")
OUT = os.path.join("evidence", "reviews_labeled.csv")


def excerpt(text, max_sentences=2, max_chars=300):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    out = " ".join(parts[:max_sentences])
    return out if len(out) <= max_chars else out[:max_chars].rsplit(" ", 1)[0] + "…"


def main():
    with open(IN, encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f)
                if int(r["so_sao"]) <= 2 and len(r["noi_dung"]) > MIN_LEN]
    rng = random.Random(SEED)
    groups = {"VN": [r for r in rows if r["thi_truong"] == "VN"],
              "US+UK": [r for r in rows if r["thi_truong"] in ("US", "UK")]}
    sample = []
    for g, rs in groups.items():
        rs = sorted(rs, key=lambda r: r["review_id"])  # thứ tự cố định trước khi xáo
        pick = rng.sample(rs, min(SAMPLE_PER_MARKET, len(rs)))
        print(f"{g}: {len(rs)} review 1–2 sao đủ dài → lấy {len(pick)}")
        sample += pick
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stt", "app", "thi_truong", "ngay", "so_sao", "trich",
                    "nhan_khoa_giu", "nhan_lua_dao", "nhan_ho_tro_kem", "nhan_khac", "ghi_chu"])
        for i, r in enumerate(sample, 1):
            w.writerow([i, r["app"], r["thi_truong"], r["ngay"], r["so_sao"],
                        excerpt(r["noi_dung"]), "", "", "", "", ""])
    print(f"{len(sample)} review → {OUT}")


if __name__ == "__main__":
    main()
