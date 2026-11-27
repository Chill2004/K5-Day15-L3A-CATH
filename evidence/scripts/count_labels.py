"""Đếm kết quả gắn nhãn tay trong evidence/reviews_labeled.csv.

Mỗi cột nhan_* điền 1 (có) hoặc để trống / 0 (không). Một review có thể mang nhiều nhãn.
Mẫu số N = mọi review trong mẫu, kể cả review không liên quan (guide 1.2).

Chạy:  python evidence/scripts/count_labels.py
Chỉ dùng thư viện chuẩn của Python.
"""
import csv
import os

IN = os.path.join("evidence", "reviews_labeled.csv")
LABELS = ["nhan_khoa_giu", "nhan_lua_dao", "nhan_ho_tro_kem", "nhan_khac"]


def is_on(v):
    return (v or "").strip() in ("1", "x", "X")


def report(rows, title):
    n = len(rows)
    if not n:
        return
    print(f"\n== {title}: N={n} ==")
    for lab in LABELS:
        x = sum(is_on(r[lab]) for r in rows)
        print(f"  {lab:18s} {x:4d}/{n} ({x / n:5.1%})")
    e3 = sum(is_on(r["nhan_khoa_giu"]) or is_on(r["nhan_lua_dao"]) for r in rows)
    print(f"  {'khoa_giu HOẶC lua_dao':18s} {e3:4d}/{n} ({e3 / n:5.1%})")
    unlabeled = sum(not any(is_on(r[l]) for l in LABELS) for r in rows)
    if unlabeled:
        print(f"  ⚠️ còn {unlabeled} review chưa gắn nhãn nào")


def main():
    with open(IN, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    report(rows, "Cả mẫu")
    report([r for r in rows if r["thi_truong"] == "VN"], "VN")
    report([r for r in rows if r["thi_truong"] in ("US", "UK")], "US+UK")


if __name__ == "__main__":
    main()
