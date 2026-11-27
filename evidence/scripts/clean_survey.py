"""Làm sạch CSV khảo sát Google Form và đếm theo cách đếm ghi trước ở evidence/survey/questions.md.

Chạy:  python evidence/scripts/clean_survey.py evidence/raw/<file tải từ Google Form>.csv
Ra:    evidence/survey/results.csv — đã BỎ cột dấu thời gian và câu 12 (liên hệ). File này commit được.
       File gốc trong evidence/raw/ KHÔNG commit.
Chỉ dùng thư viện chuẩn của Python.
"""
import csv
import os
import sys
from collections import Counter

OUT = os.path.join("evidence", "survey", "results.csv")


def bo_cot(ten):
    t = ten.strip().lower()
    return t in ("dấu thời gian", "timestamp") or t.startswith("12.")


def tim_cot(header, so):
    for h in header:
        if h.strip().startswith("%d." % so):
            return h
    sys.exit("Không thấy cột câu %d trong file — kiểm lại tiêu đề cột." % so)


def main(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("File không có câu trả lời nào.")
    header = list(rows[0].keys())
    giu = [h for h in header if not bo_cot(h)]
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=giu)
        w.writeheader()
        for r in rows:
            w.writerow({h: r[h] for h in giu})
    print("Đã ghi %s (%d câu trả lời, bỏ cột: %s)" % (OUT, len(rows), [h for h in header if bo_cot(h)]))

    c1, c5, c7, c8, c9, c10 = (tim_cot(header, i) for i in (1, 5, 7, 8, 9, 10))
    dung = [r for r in rows if r[c1].strip() == "Có"]
    n = len(dung)
    print("\nTổng câu trả lời: %d · đúng người dùng (câu 1 = Có): N = %d" % (len(rows), n))
    if not n:
        return
    ghi_pct = n >= 10

    def bao(x, mau=None):
        mau = n if mau is None else mau
        return "%d/%d" % (x, mau) + (" (%.0f%%)" % (100 * x / mau) if ghi_pct and mau else "")

    bi_giu = [r for r in dung if r[c5].startswith("Có")]
    bi_giuc = [r for r in dung if r[c9].startswith("Có") or r[c9] == "Cả hai"]
    print("(a) Có giao dịch bị giữ/chặn trong 3 tháng qua: " + bao(len(bi_giu)))
    print("(b) Bản thân hoặc người thân bị giục chuyển tiền trong 1 tháng qua: " + bao(len(bi_giuc)))
    if bi_giu:
        print("(c) Trong %d người bị giữ:" % len(bi_giu))
        print("    thời gian xử lý (câu 7):", dict(Counter(r[c7] or "(bỏ trống)" for r in bi_giu)))
        print("    hỗ trợ giải quyết (câu 8):", dict(Counter(r[c8] or "(bỏ trống)" for r in bi_giu)))
    if bi_giuc:
        print("    chuyện gì xảy ra khi bị giục (câu 10):", dict(Counter(r[c10] or "(bỏ trống)" for r in bi_giuc)))
    if not ghi_pct:
        print("\nN < 10: chỉ ghi x/n, không ghi % (guide).")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Cách chạy: python evidence/scripts/clean_survey.py evidence/raw/<file>.csv")
    main(sys.argv[1])
