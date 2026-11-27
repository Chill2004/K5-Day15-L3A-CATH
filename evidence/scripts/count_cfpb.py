"""Đếm khiếu nại CFPB theo nhãn Issue / Sub-issue / Company.

Cách lấy file CSV (ghi trong evidence/data-mining.md):
  CFPB Consumer Complaint Database → lọc Date received 27/11/2025–27/11/2026
  + Product = "Money transfer, virtual currency, or money service" → Download data → CSV.
  Lưu vào evidence/raw/ (thư mục này không commit).

Chạy:  python evidence/scripts/count_cfpb.py evidence/raw/<file>.csv
Chỉ dùng thư viện chuẩn của Python.
"""
import csv
import sys
from collections import Counter

# Nhãn CFPB nhóm coi là liên quan tới hướng E3 (giao dịch bị giữ / lừa đảo / không dùng được tiền).
E3_ISSUES = {
    "Fraud or scam",
    "Unauthorized transactions or other transaction problem",
    "Trouble accessing funds in your mobile or digital wallet",
}


def pct(x, n):
    return f"{x:6d}/{n} ({x / n:5.1%})"


def main(path):
    csv.field_size_limit(10**9)
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    n = len(rows)
    dates = sorted(r["Date received"] for r in rows if r.get("Date received"))
    products = Counter(r["Product"] for r in rows)
    print(f"File: {path}")
    print(f"Số dòng (N): {n}")
    print(f"Ngày nhận: {dates[0]} → {dates[-1]}")
    print(f"Product: {dict(products)}")

    print("\n== Theo Issue ==")
    issues = Counter(r["Issue"] for r in rows)
    for k, c in issues.most_common():
        print(f"  {pct(c, n)}  {k}")

    e3 = sum(c for k, c in issues.items() if k in E3_ISSUES)
    fraud_unauth = issues["Fraud or scam"] + issues["Unauthorized transactions or other transaction problem"]
    print("\n== Gộp ==")
    print(f"  Lừa đảo + giao dịch trái phép:        {pct(fraud_unauth, n)}")
    print(f"  Ba nhãn E3 (thêm không dùng được tiền): {pct(e3, n)}")

    print("\n== Sub-issue của ba nhãn E3 (top 15) ==")
    subs = Counter((r["Issue"], r["Sub-issue"]) for r in rows if r["Issue"] in E3_ISSUES)
    for (iss, sub), c in subs.most_common(15):
        print(f"  {c:6d}  {iss[:30]:30s} · {sub or '(trống)'}")

    print("\n== Company, ba nhãn E3 (top 10) ==")
    comp = Counter(r["Company"] for r in rows if r["Issue"] in E3_ISSUES)
    for k, c in comp.most_common(10):
        print(f"  {c:6d}  {k}")

    narr = sum(1 for r in rows if (r.get("Consumer complaint narrative") or "").strip())
    print(f"\nCó lời kể (narrative): {pct(narr, n)}")
    resp = Counter(r["Company response to consumer"] for r in rows)
    print(f"Company response: {dict(resp)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Cách chạy: python evidence/scripts/count_cfpb.py <file.csv>")
    main(sys.argv[1])
