"""So nhãn nhom + hanh_dong trong output với cột expected — hỗ trợ chấm metric dung_huong_xu_ly.

Chỉ so PHẦN NHÃN (khớp chính xác). Phần tra_loi vẫn do người chấm theo pass_criterion và
eval/metric_spec.yaml. Script KHÔNG ghi vào file kết quả (không sửa eval/run-*.csv).

Chạy:  python eval/so_nhan.py eval/run-try.csv
       python eval/so_nhan.py eval/run-1.csv
Chỉ dùng thư viện chuẩn của Python.
"""
import csv
import json
import re
import sys


def doc_nhan(output):
    """Output của agent là chuỗi JSON {nhom, hanh_dong, tra_loi, tom_tat}; bản cũ là dòng [nhom=… · hanh_dong=…]."""
    try:
        o = json.loads(output)
        return o.get("nhom"), o.get("hanh_dong"), o.get("tra_loi", "")
    except (ValueError, TypeError, AttributeError):
        m = re.search(r"nhom=(\w+).*?hanh_dong=(\w+)", output or "")
        return (m.group(1), m.group(2), output) if m else (None, None, output)


def main(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    dung, loi, lech = 0, [], []
    for r in rows:
        if (r.get("error") or "").strip():
            loi.append((r["id"], r["error"][:100]))
            continue
        exp = json.loads(r["expected"])
        nhom, hd, tl = doc_nhan(r["output"])
        if nhom == exp.get("nhom") and hd == exp.get("hanh_dong"):
            dung += 1
        else:
            lech.append((r["id"], r.get("type", ""), exp, nhom, hd, tl))
    n = len(rows)
    print("File: %s · %d câu" % (path, n))
    print("Khớp cả nhom + hanh_dong: %d/%d (%.0f%%) · lỗi chạy: %d (tính trượt)" % (dung, n, 100 * dung / n if n else 0, len(loi)))
    for i, e in loi:
        print("  LỖI %s: %s" % (i, e))
    for i, t, exp, nhom, hd, tl in lech:
        print("\n  LỆCH %s [%s] mong %s/%s · ra %s/%s" % (i, t, exp.get("nhom"), exp.get("hanh_dong"), nhom, hd))
        print("       tra_loi: %s" % (tl or "")[:240])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Cách chạy: python eval/so_nhan.py eval/run-try.csv")
    main(sys.argv[1])
