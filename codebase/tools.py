"""Công cụ của bài toán — NHÓM VIẾT. Điền ở guide bước 2.2 (thiết kế) và 3.2 (code).

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý như sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không (gửi tin, sửa dữ liệu, chấm điểm…)
Khung tự ghi mỗi lần gọi công cụ vào trace (tên, input, output rút gọn, thời gian, lỗi).

Công cụ có tác động ra ngoài: KHÔNG tự làm. Trả về bản nháp chờ người duyệt (guide bước 2.2).
Dữ liệu: để trong data/ và mô tả ở data/DATA_CARD.md.

CP3 hook: đặt data/held_transactions.json → get_held_transaction tự đọc, không đổi signature.
"""
import json
import os

from tracing import tool, TOOLS  # noqa: F401


# ---------------------------------------------------------------------------
# Dữ liệu mock cho CP2 — phiên chat mở từ thông báo giao dịch bị tạm giữ
# CP3: đặt data/held_transactions.json với cùng schema → tự dùng file thật
# ---------------------------------------------------------------------------

_MOCK_GD = [
    {
        "tx_id": "TX-2026-0001",
        "so_tien": "2.500.000 đ",
        "nguoi_nhan": "NGUYEN VAN A",
        "loai_nguoi_nhan": "tài khoản lần đầu nhận tiền từ bạn",
        "thoi_gian": "2026-11-27T19:45:00+07:00",
        "trang_thai": "đang tạm giữ",
    },
    {
        "tx_id": "TX-2026-0002",
        "so_tien": "8.000.000 đ",
        "nguoi_nhan": "Trường ĐH Bách Khoa HN",
        "loai_nguoi_nhan": "tổ chức giáo dục đã xác minh",
        "thoi_gian": "2026-11-27T20:10:00+07:00",
        "trang_thai": "đang tạm giữ",
    },
    {
        "tx_id": "TX-2026-0003",
        "so_tien": "15.000.000 đ",
        "nguoi_nhan": "Người lạ",
        "loai_nguoi_nhan": "tài khoản lần đầu nhận tiền từ bạn",
        "thoi_gian": "2026-11-27T20:30:00+07:00",
        "trang_thai": "đang tạm giữ",
    },
]

# Các khoá được phép truyền vào classify (theo decide.py → _mo_ta_giao_dich)
_CLASSIFY_KEYS = {"tx_id", "so_tien", "nguoi_nhan", "loai_nguoi_nhan", "thoi_gian", "trang_thai"}


def _load_gd_list() -> list:
    """CP3 hook: đọc data/held_transactions.json nếu tồn tại, ngược lại dùng mock."""
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "held_transactions.json",
    )
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return _MOCK_GD


def _match(hint: str, records: list):
    """Trả giao dịch của phiên chat:
    Nếu hint có mã TX-... khớp trực tiếp thì trả giao dịch đó;
    ngược lại mặc định trả giao dịch đang giữ của phiên (records[0])."""
    if not records:
        return None
    h_lower = (hint or "").lower()
    for rec in records:
        tx_id = rec.get("tx_id", "")
        if tx_id and tx_id.lower() in h_lower:
            return rec
    return records[0]


# ---------------------------------------------------------------------------
# Công cụ 1 — Tra giao dịch bị giữ
# ---------------------------------------------------------------------------

@tool
def get_held_transaction(user_hint: str) -> dict:
    """Tra cứu giao dịch đang bị ví tạm giữ dựa trên gợi ý từ người dùng.

    Tên/mục đích: Lấy thông tin giao dịch đang bị tạm giữ để agent có căn cứ
        gọi classify(). Trả về đủ các khoá classify cần, không trả ngưỡng
        hoặc điểm rủi ro nội bộ.
    Input: user_hint (str) — đoạn mô tả ngắn từ người dùng (mã giao dịch,
        số tiền, tên người nhận, từ khoá liên quan…); có thể rỗng hoặc thiếu.
    Output: dict —
        Tìm thấy: {"found": True, "tx_id", "so_tien", "nguoi_nhan",
            "loai_nguoi_nhan", "thoi_gian", "trang_thai"}
        Không tìm thấy: {"found": False, "tx_id": None,
            "note": "Không tìm thấy giao dịch"}
    Tác động ra ngoài: Không — chỉ đọc dữ liệu, không thay đổi trạng thái.
    """
    if not user_hint or not user_hint.strip():
        return {"found": False, "tx_id": None, "note": "Không tìm thấy giao dịch"}

    rec = _match(user_hint.strip(), _load_gd_list())
    if rec is None:
        return {"found": False, "tx_id": None, "note": "Không tìm thấy giao dịch"}

    # Chỉ trả các khoá classify cho phép + found flag
    result = {"found": True}
    for k in _CLASSIFY_KEYS:
        if k in rec:
            result[k] = rec[k]
    return result


def get_held_transaction_for_classify(gd_raw: dict) -> dict:
    """Helper: lọc dict giao dịch, chỉ giữ khoá classify cho phép.
    Dùng trong agent.py trước khi gọi classify(tin_nhan, gd_for_classify).
    Không phải @tool — không cần ghi trace riêng."""
    return {k: v for k, v in (gd_raw or {}).items() if k in _CLASSIFY_KEYS}


# ---------------------------------------------------------------------------
# Công cụ 2 — Giữ tiếp + cảnh báo (bi_giuc_chuyen)
# ---------------------------------------------------------------------------

@tool
def hold_transaction(tx_id: str, ly_do: str = "") -> dict:
    """Xác nhận giữ tiếp giao dịch và tạo nội dung cảnh báo cho người dùng.

    Tên/mục đích: Dùng khi agent quyết định giữ tiếp giao dịch
        (nhóm bi_giuc_chuyen). Không thay đổi trạng thái thật của giao dịch;
        guard.py đã đảm bảo câu trả lời người dùng đúng chuẩn.
    Input:
        tx_id (str) — mã giao dịch bị giữ.
        ly_do (str, tuỳ chọn) — lý do phân loại (ghi vào trace).
    Output: dict — {"action": "hold_transaction", "tx_id": str,
        "status": "confirmed_hold", "ly_do": str}
    Tác động ra ngoài: Không — xác nhận trong bộ nhớ, không gửi lệnh API.
    """
    return {
        "action": "hold_transaction",
        "tx_id": tx_id,
        "status": "confirmed_hold",
        "ly_do": ly_do,
    }


# ---------------------------------------------------------------------------
# Công cụ 3 — Gửi màn hình xác thực (gap_that)
# ---------------------------------------------------------------------------

@tool
def request_verification(tx_id: str, phuong_thuc: str = "face_scan") -> dict:
    """Tạo bước xác thực danh tính cho giao dịch khẩn cấp thật sự.

    Tên/mục đích: Dùng khi agent quyết định gửi xác thực (nhóm gap_that).
        Chỉ tạo bước xác thực — KHÔNG nhả tiền hay thay đổi trạng thái thật.
        Màn hình xác thực hiện ngay trong ứng dụng ví (không gửi link ngoài).
    Input:
        tx_id (str) — mã giao dịch cần xác thực.
        phuong_thuc (str) — phương thức: "face_scan" (mặc định),
            "callback" (gọi về số đăng ký), "otp_device" (OTP thiết bị đăng ký).
    Output: dict — {"action": "request_verification", "tx_id": str,
        "phuong_thuc": str, "status": "draft",
        "requires_human_approval": False}
    Tác động ra ngoài: Không — chỉ tạo bản nháp bước xác thực trong bộ nhớ.
    """
    return {
        "action": "request_verification",
        "tx_id": tx_id,
        "phuong_thuc": phuong_thuc,
        "status": "draft",
        "requires_human_approval": False,
    }


# ---------------------------------------------------------------------------
# Công cụ 4 — Chuyển tư vấn viên (nghi_chiem_tk / chua_ro / ngoài phạm vi)
# ---------------------------------------------------------------------------

@tool
def handoff_to_agent(tx_id: str, tom_tat: str, suggested_action: str = "") -> dict:
    """Tạo bản nháp chuyển ca lên tư vấn viên kèm tóm tắt tình huống.

    Tên/mục đích: Dùng khi agent quyết định chuyển tư vấn viên
        (nhóm nghi_chiem_tk, chua_ro hoặc ca ngoài phạm vi).
        Luôn trả requires_human_approval=True; không thực thi hành động thật.
    Input:
        tx_id (str) — mã giao dịch liên quan.
        tom_tat (str) — tóm tắt 1–2 câu để tư vấn viên nắm ngay tình huống.
        suggested_action (str, tuỳ chọn) — hành động đề xuất tư vấn viên
            xem xét (ví dụ: "khoa_vi_tam_thoi", "nha_giao_dich").
    Output: dict — {"action": "handoff_to_agent", "tx_id": str,
        "tom_tat": str, "suggested_action": str,
        "status": "draft", "requires_human_approval": True}
    Tác động ra ngoài: Không — chỉ tạo bản nháp; tư vấn viên phải duyệt.
        requires_human_approval luôn là True.
    """
    return {
        "action": "handoff_to_agent",
        "tx_id": tx_id,
        "tom_tat": tom_tat,
        "suggested_action": suggested_action,
        "status": "draft",
        "requires_human_approval": True,
    }


# ---------------------------------------------------------------------------
# Công cụ bị chặn — chỉ được tạo bản nháp, KHÔNG thực thi thật
# (guard.py chan_cong_cu() chặn trước khi hàm này chạy)
# ---------------------------------------------------------------------------

@tool
def release_transaction(tx_id: str, ly_do: str = "") -> dict:
    """CÔNG CỤ BỊ CHẶN — AI không được tự gọi.

    Tên/mục đích: Nhả giao dịch bị giữ — chỉ tạo bản nháp chờ tư vấn viên duyệt.
        guard.py chan_cong_cu("release_transaction") chặn hàm này trước khi chạy
        và trả bản nháp thay thế. Nếu hàm này vẫn được gọi trực tiếp (không qua
        chan_cong_cu), nó cũng chỉ trả bản nháp — không thực thi thật.
    Input: tx_id (str), ly_do (str, tuỳ chọn).
    Output: dict — {"action": "release_transaction", "tx_id": str, "ly_do": str,
        "status": "draft", "requires_human_approval": True,
        "trang_thai": "cho_duyet"}
    Tác động ra ngoài: Không — KHÔNG nhả tiền thật, chỉ tạo bản nháp.
    """
    # Lớp bảo vệ thứ hai: ngay cả khi chan_cong_cu không được gọi,
    # hàm này vẫn trả bản nháp thay vì thực thi thật.
    return {
        "action": "release_transaction",
        "tx_id": tx_id,
        "ly_do": ly_do,
        "status": "draft",
        "requires_human_approval": True,
        "trang_thai": "cho_duyet",
    }


def _strip_accents(text: str) -> str:
    """Chuyển chuỗi tiếng Việt về dạng không dấu để so sánh linh hoạt hơn."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


# ---------------------------------------------------------------------------
# Dữ liệu mock cho CP2 — CP3 đọc từ data/held_transactions.json nếu tồn tại
# ---------------------------------------------------------------------------

_MOCK_TRANSACTIONS = [
    {
        "tx_id": "TX-2026-0001",
        "user_hint_keywords": ["0001", "momo", "chuyển tiền", "bị giữ", "hôm nay"],
        "amount": 2500000,
        "currency": "VND",
        "recipient": "Nguyễn Văn A",
        "status": "held",
        "hold_reason": "nghi_lua_dao",        # bị giục chuyển tiền
        "hold_reason_label": "Nghi lừa đảo — người thụ hưởng thuộc danh sách cảnh báo",
        "timestamp": "2026-11-27T19:45:00+07:00",
    },
    {
        "tx_id": "TX-2026-0002",
        "user_hint_keywords": ["0002", "tiền học phí", "học phí", "khẩn", "gấp"],
        "amount": 8000000,
        "currency": "VND",
        "recipient": "Trường ĐH Bách Khoa",
        "status": "held",
        "hold_reason": "vuot_han_muc",         # gấp thật — vượt hạn mức giao dịch
        "hold_reason_label": "Vượt hạn mức giao dịch trong ngày",
        "timestamp": "2026-11-27T20:10:00+07:00",
    },
    {
        "tx_id": "TX-2026-0003",
        "user_hint_keywords": ["0003", "lạ", "không phải tôi", "chiếm", "tài khoản bị"],
        "amount": 15000000,
        "currency": "VND",
        "recipient": "Người lạ",
        "status": "held",
        "hold_reason": "nghi_chiem_tai_khoan",  # nghi chiếm tài khoản
        "hold_reason_label": "Giao dịch bất thường — nghi chiếm đoạt tài khoản",
        "timestamp": "2026-11-27T20:30:00+07:00",
    },
]


def _load_transactions() -> list:
    """CP3 hook: đọc data/held_transactions.json nếu tồn tại, ngược lại dùng mock.
    Không thay đổi signature của lookup_held_transaction."""
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "held_transactions.json"
    )
    if os.path.isfile(data_path):
        with open(data_path, encoding="utf-8") as f:
            return json.load(f)
    return _MOCK_TRANSACTIONS


def _match_transaction(user_hint: str, transactions: list) -> dict | None:
    """Tìm giao dịch khớp user_hint qua keyword (có dấu và không dấu)."""
    hint_lower = user_hint.lower()
    hint_stripped = _strip_accents(user_hint)
    for tx in transactions:
        # Khớp trực tiếp tx_id
        if tx.get("tx_id", "").lower() in hint_lower:
            return tx
        for kw in tx.get("user_hint_keywords", []):
            kw_lower = kw.lower()
            kw_stripped = _strip_accents(kw)
            # Khớp có dấu hoặc không dấu (cả chiều: hint chứa keyword hoặc keyword chứa trong hint)
            if kw_lower in hint_lower or kw_stripped in hint_stripped:
                return tx
    return None


# ---------------------------------------------------------------------------
# Công cụ 1 — Tra giao dịch bị giữ
# ---------------------------------------------------------------------------

@tool
def lock_wallet(tx_id: str, ly_do: str = "") -> dict:
    """CÔNG CỤ BỊ CHẶN — AI không được tự gọi.

    Tên/mục đích: Khoá ví/tài khoản — chỉ tạo bản nháp chờ tư vấn viên duyệt.
        guard.py chan_cong_cu("lock_wallet") chặn hàm này trước khi chạy.
        Nếu hàm này vẫn được gọi trực tiếp, cũng chỉ trả bản nháp.
    Input: tx_id (str), ly_do (str, tuỳ chọn).
    Output: dict — {"action": "lock_wallet", "tx_id": str, "ly_do": str,
        "status": "draft", "requires_human_approval": True,
        "trang_thai": "cho_duyet"}
    Tác động ra ngoài: Không — KHÔNG khoá ví thật, chỉ tạo bản nháp.
    """
    return {
        "action": "lock_wallet",
        "tx_id": tx_id,
        "ly_do": ly_do,
        "status": "draft",
        "requires_human_approval": True,
        "trang_thai": "cho_duyet",
    }
