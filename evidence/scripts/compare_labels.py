"""So nhãn của người gắn thứ hai (40 review) với bảng nhãn chính.

Một review "khớp" khi cả 4 cột nhan_* giống nhau. Ngưỡng ghi trong evidence/data-mining.md:
lệch ≥ 8/40 review thì định nghĩa nhãn còn mơ hồ → viết lại rồi gắn lại.

Chạy:  python evidence/scripts/compare_labels.py
Chỉ dùng thư viện chuẩn của Python.
"""
import csv
import os

MAIN = os.path.join("evidence", "reviews_labeled.csv")
CHECK = os.path.join("evidence", "reviews_check_ha.csv")
LABELS = ["nhan_khoa_giu", "nhan_lua_dao", "nhan_ho_tro_kem", "nhan_khac"]


def on(v):
    return (v or "").strip() in ("1", "x", "X")


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return {r["stt"]: r for r in csv.DictReader(f)}


def main():
    main_rows, check_rows = load(MAIN), load(CHECK)
    same, diffs = 0, []
    for stt, c in check_rows.items():
        m = main_rows[stt]
        a = tuple(on(m[l]) for l in LABELS)
        b = tuple(on(c[l]) for l in LABELS)
        if a == b:
            same += 1
        else:
            diffs.append((stt, a, b, m["trich"][:90]))
    n = len(check_rows)
    print(f"Khớp {same}/{n} review · lệch {n - same}/{n} (ngưỡng: lệch ≥ 8 thì viết lại định nghĩa)")
    for lab_i, lab in enumerate(LABELS):
        agree = sum(on(main_rows[s][lab]) == on(c[lab]) for s, c in check_rows.items())
        print(f"  {lab:18s} khớp {agree}/{n}")
    if diffs:
        print("\nCác review lệch (chính → người kiểm), thứ tự: khoa_giu, lua_dao, ho_tro_kem, khac")
        for stt, a, b, t in diffs:
            print(f"  stt {stt}: {''.join('1' if x else '0' for x in a)} → {''.join('1' if x else '0' for x in b)} · {t}")


if __name__ == "__main__":
    main()
