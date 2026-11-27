"""Lấy review Google Play mới nhất của app ví / ngân hàng → CSV thô.

Chạy:  pip install google-play-scraper
       python evidence/scripts/scrape_reviews.py
Ra:    evidence/raw/reviews_raw.csv  (KHÔNG commit — luật chỉ cho trích ≤2 câu mỗi review)

Không lưu tên người viết review. Ghi lại ngày chạy trong evidence/data-mining.md.
"""
import csv
import os
from datetime import date

from google_play_scraper import Sort, reviews

COUNT_PER_APP = 1000

# (tên app, package id, ngôn ngữ, quốc gia, thị trường)
APPS = [
    ("MoMo", "com.mservice.momotransfer", "vi", "vn", "VN"),
    ("ZaloPay", "vn.com.vng.zalopay", "vi", "vn", "VN"),
    ("MB Bank", "com.mbmobile", "vi", "vn", "VN"),
    ("Vietcombank", "com.VCB", "vi", "vn", "VN"),
    ("Techcombank", "vn.com.techcombank.bb.app", "vi", "vn", "VN"),
    ("VietinBank", "com.vietinbank.ipay", "vi", "vn", "VN"),
    ("BIDV", "com.vnpay.bidv", "vi", "vn", "VN"),
    ("TPBank", "com.tpb.mb.gprsandroid", "vi", "vn", "VN"),
    ("Cash App", "com.squareup.cash", "en", "us", "US"),
    ("Chime", "com.onedebit.chime", "en", "us", "US"),
    ("Venmo", "com.venmo", "en", "us", "US"),
    ("PayPal", "com.paypal.android.p2pmobile", "en", "us", "US"),
    ("Revolut", "com.revolut.revolut", "en", "gb", "UK"),
    ("Monzo", "co.uk.getmondo", "en", "gb", "UK"),
    ("Wise", "com.transferwise.android", "en", "gb", "UK"),
]

OUT = os.path.join("evidence", "raw", "reviews_raw.csv")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    n = 0
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["review_id", "app", "thi_truong", "ngay", "so_sao", "noi_dung", "ngay_lay"])
        for name, pid, lang, country, market in APPS:
            rs, _ = reviews(pid, lang=lang, country=country, sort=Sort.NEWEST, count=COUNT_PER_APP)
            for r in rs:
                w.writerow([r["reviewId"], name, market, str(r["at"])[:10], r["score"],
                            (r["content"] or "").replace("\n", " ").strip(), date.today().isoformat()])
            n += len(rs)
            first = str(rs[-1]["at"])[:10] if rs else "-"
            last = str(rs[0]["at"])[:10] if rs else "-"
            print(f"{name:12s} {market}  N={len(rs):5d}  {first} → {last}")
    print(f"Tổng {n} review → {OUT}")


if __name__ == "__main__":
    main()
