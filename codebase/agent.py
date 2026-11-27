"""Luồng chính của bản chạy thử — E3: hỗ trợ ví điện tử khi giao dịch bị tạm giữ.

`python run.py`, `python run.py eval` và `python run.py simulate` đều gọi answer(text).

Hợp đồng:
    answer(text: str) -> dict có khoá "output" (str): kết quả đưa cho người dùng.
    Token, tên model, số lần gọi model / công cụ: khung tự đếm qua @model_call và @tool.

Luồng (workflow cố định, xem spec.md §4):
    1. get_held_transaction(text)   — tra giao dịch; nếu không thấy → hỏi lại (G10)
    2. classify(text, gd)           — model phân loại + chọn hành động
    3. guard(kq, text, gd)          — kiểm bằng code, lọc vi phạm, đảm bảo luật cứng
    4. dispatch theo g["hanh_dong"] — gọi đúng tool action tương ứng
    5. return {"output": g["tra_loi"]}

KHÔNG sửa codebase/decide.py, codebase/guard.py, codebase/ai.py (của Cường).
"""
from tracing import note

from decide import classify
from guard import chan_cong_cu, guard
from tools import (
    get_held_transaction,
    get_held_transaction_for_classify,
    handoff_to_agent,
    hold_transaction,
    request_verification,
)

# Câu hỏi lại mặc định khi không tìm thấy giao dịch (G10 — hỏi đúng 1 câu)
_HOI_LAI_KHONG_THAY_GD = (
    "Mình chưa tìm thấy giao dịch của bạn. "
    "Bạn cho mình biết mã giao dịch, số tiền, hoặc tên người nhận "
    "được không? (Thông tin này in trong thông báo bạn vừa nhận.)"
)


def answer(text: str) -> dict:
    """Phân loại tin nhắn của người dùng và chọn hành động phù hợp.

    Trả {"output": str} — câu trả lời đã qua guard (đảm bảo luật cứng).
    """
    # ------------------------------------------------------------------
    # Bước 1: Tra giao dịch bị giữ của phiên chat
    # ------------------------------------------------------------------
    gd_raw = get_held_transaction(text)
    gd = get_held_transaction_for_classify(gd_raw) if gd_raw.get("found") else None

    # ------------------------------------------------------------------
    # Bước 2: Classify — luôn gọi model (kể cả khi gd=None)
    # ------------------------------------------------------------------
    kq = classify(text, gd)

    # ------------------------------------------------------------------
    # Bước 3: Guard — kiểm bằng code sau khi model trả lời
    # ------------------------------------------------------------------
    g = guard(kq, text, gd)

    # ------------------------------------------------------------------
    # Bước 4: Dispatch — gọi tool action tương ứng hanh_dong
    # ------------------------------------------------------------------
    nhom = kq.get("nhom", "chua_ro")
    hanh_dong = g.get("hanh_dong", "chuyen_tu_van_vien")
    tx_id = (gd or {}).get("tx_id", "")

    if hanh_dong == "giu_va_canh_bao":
        draft = chan_cong_cu("hold_transaction", gd)
        if draft is None:
            hold_transaction(tx_id, ly_do=kq.get("ly_do", ""))
        note("agent: dispatch → giu_va_canh_bao · tx=%s" % tx_id)

    elif hanh_dong == "gui_xac_thuc":
        draft = chan_cong_cu("request_verification", gd)
        if draft is None:
            request_verification(tx_id)
        note("agent: dispatch → gui_xac_thuc · tx=%s" % tx_id)

    elif hanh_dong == "hoi_lai":
        note("agent: dispatch → hoi_lai · tx=%s" % tx_id)

    elif hanh_dong == "chuyen_tu_van_vien":
        draft = chan_cong_cu("handoff_to_agent", gd)
        if draft is None:
            handoff_to_agent(
                tx_id=tx_id,
                tom_tat=kq.get("tom_tat", ""),
                suggested_action="",
            )
        note("agent: dispatch → chuyen_tu_van_vien · tx=%s" % tx_id)

    # ------------------------------------------------------------------
    # Bước 5: Trả kết quả kèm [nhom=... · hanh_dong=...]
    # ------------------------------------------------------------------
    tra_loi = g.get("tra_loi") or ""
    if not tra_loi:
        tra_loi = (
            "Mình đã nhận yêu cầu của bạn. Giao dịch vẫn đang được giữ an toàn, "
            "bạn vui lòng chờ trong giây lát."
        )
        note("agent: tra_loi rỗng — dùng fallback")

    return {"output": "[nhom=%s · hanh_dong=%s]\n%s" % (nhom, hanh_dong, tra_loi)}
