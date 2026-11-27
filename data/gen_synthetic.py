"""Sinh data GIẢ cho bản chạy thử — nhãn synthetic. Chạy lại cùng seed ra đúng cùng file.

    python data/gen_synthetic.py            # seed 42 → data/held_transactions.csv, data/messages.csv

Mọi tên, số tài khoản, số tiền đều bịa, KHÔNG phải dữ liệu thật và KHÔNG phải bằng chứng pain.
Chỉ dùng thư viện chuẩn.
"""
import csv
import datetime
import os
import random
import sys

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 42
N_TX = 30
HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(SEED)

# Lý do ví tạm giữ (mô tả cho tư vấn viên; KHÔNG chứa ngưỡng phát hiện — ngưỡng nằm trong code, AI không đọc)
HOLD_REASONS = ["nguoi_nhan_moi", "so_tien_bat_thuong", "thiet_bi_moi", "nguoi_nhan_bi_bao_cao", "gio_bat_thuong"]
RECIPIENT_TYPES = ["ca_nhan", "cua_hang", "vi_khac", "ngan_hang"]
CHANNELS = ["chuyen_vi", "chuyen_ngan_hang", "thanh_toan_qr"]

# Tin nhắn mẫu theo 4 nhóm của lát cắt. Nhóm tự viết, lấy ý từ kiểu phàn nàn đọc được trong review
# (evidence/data-mining.md §2) — không chép nguyên văn review.
MESSAGES = {
    "bi_giuc": [
        "Bên công an gọi bảo tôi chuyển gấp vào tài khoản an toàn, sao ví lại chặn, mở cho tôi ngay",
        "Người bên sàn đầu tư bảo phải nộp phí trong 10 phút không thì mất hết tiền gốc, giúp tôi với",
        "Nhân viên ngân hàng đang giữ máy với tôi, bảo đọc mã cho họ rồi chuyển lại, sao không chuyển được",
        "Shop bảo chuyển cọc trước 15 phút nữa là hết hàng, mở giao dịch giúp em",
        "Có người nhắn là con tôi bị tai nạn cần tiền viện phí ngay, đừng chặn tôi",
    ],
    "gap_that": [
        "Em đang ở bệnh viện cần đóng tiền cho mẹ, tài khoản bệnh viện em chuyển mọi lần rồi mà giờ bị giữ",
        "Tôi trả tiền nhà cho chủ trọ tháng nào cũng chuyển, hôm nay bị chặn, chủ nhà đang đứng đợi",
        "Thanh toán tiền hàng cho nhà cung cấp quen, hạn chót trong hôm nay, xác thực giúp tôi được không",
        "Mình chuyển học phí cho con, trường đóng cổng thu lúc 17h",
    ],
    "chiem_tk": [
        "Tôi không hề tạo giao dịch này, sao ví báo đang giữ khoản chuyển 5 triệu",
        "Vừa nhận tin đăng nhập trên máy lạ, sau đó thấy có lệnh chuyển tiền bị giữ, tôi không làm",
        "Ai đó đổi số điện thoại trong ví của tôi, giờ có giao dịch lạ bị chặn",
    ],
    "chua_ro": [
        "Sao bị giữ vậy",
        "Giao dịch của tôi đâu rồi",
        "Mở giúp với",
        "Ủa lỗi gì thế",
    ],
}


def fake_amount():
    return rng.choice([150_000, 500_000, 1_200_000, 2_000_000, 3_500_000, 5_000_000, 10_000_000, 20_000_000])


def main():
    start = datetime.datetime(2026, 11, 20, 0, 0)
    tx_rows, msg_rows = [], []
    # Chia gần đều 4 nhóm (bi_giuc nhiều nhất vì là ca rủi ro mất tiền), rồi xáo theo seed
    order = (["bi_giuc"] * 9 + ["gap_that"] * 8 + ["chiem_tk"] * 7 + ["chua_ro"] * 6)[:N_TX]
    rng.shuffle(order)
    for i in range(1, N_TX + 1):
        nhom = order[i - 1]
        tx_id = "TX%04d" % i
        t = start + datetime.timedelta(minutes=rng.randint(0, 7 * 24 * 60))
        tx_rows.append({
            "tx_id": tx_id,
            "user_id": "U%03d" % rng.randint(1, 200),
            "thoi_gian": t.strftime("%Y-%m-%d %H:%M"),
            "so_tien_vnd": fake_amount(),
            "kenh": rng.choice(CHANNELS),
            "loai_nguoi_nhan": rng.choice(RECIPIENT_TYPES),
            "nguoi_nhan_da_chuyen_truoc": "co" if nhom == "gap_that" else rng.choice(["co", "khong"]),
            "thiet_bi_moi": "co" if nhom == "chiem_tk" else rng.choice(["co", "khong", "khong"]),
            "ly_do_giu": rng.choice(HOLD_REASONS),
            "trang_thai": "dang_giu",
            "nhom_that": nhom,          # nhãn đúng để chấm — agent KHÔNG được đọc cột này
            "nhan": "synthetic",
        })
        msg_rows.append({
            "msg_id": "M%04d" % i,
            "tx_id": tx_id,
            "tin_nhan": rng.choice(MESSAGES[nhom]),
            "nhom_that": nhom,
            "ngoai_gio": "co" if t.hour >= 20 or t.hour < 8 else "khong",
            "nguon": "tu_viet",
            "nhan": "synthetic",
        })
    for name, rows in (("held_transactions.csv", tx_rows), ("messages.csv", msg_rows)):
        with open(os.path.join(HERE, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print("Đã ghi data/%s (%d dòng, seed %d)" % (name, len(rows), SEED))


if __name__ == "__main__":
    main()
