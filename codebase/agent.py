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
    # Bước 1: Tra giao dịch bị giữ
    # ------------------------------------------------------------------
    gd_raw = get_held_transaction(text)

    if not gd_raw.get("found"):
        # G10: không tìm thấy giao dịch → hỏi lại đúng 1 câu, không bịa tx_id
        note("agent: không tìm thấy giao dịch — hỏi lại (G10)")
        return {"output": _HOI_LAI_KHONG_THAY_GD}

    # Lọc giao dịch: chỉ giữ khoá classify cho phép
    # (không truyền ngưỡng rủi ro hay _keywords vào model)
    gd = get_held_transaction_for_classify(gd_raw)

    # ------------------------------------------------------------------
    # Bước 2: Classify — model phân loại tin nhắn + chọn hành động
    # ------------------------------------------------------------------
    kq = classify(text, gd)

    # ------------------------------------------------------------------
    # Bước 3: Guard — kiểm bằng code sau khi model trả lời
    # ------------------------------------------------------------------
    g = guard(kq, text, gd)

    # ------------------------------------------------------------------
    # Bước 4: Dispatch — gọi tool action tương ứng hanh_dong
    # ------------------------------------------------------------------
    hanh_dong = g.get("hanh_dong", "chuyen_tu_van_vien")
    tx_id = gd.get("tx_id", "")

    if hanh_dong == "giu_va_canh_bao":
        # Trước khi gọi, kiểm chan_cong_cu phòng trường hợp sau này
        # agent mở rộng và vô tình gọi tool cấm
        draft = chan_cong_cu("hold_transaction", gd)
        if draft is None:   # hold_transaction không phải công cụ cấm
            hold_transaction(tx_id, ly_do=kq.get("ly_do", ""))
        note("agent: dispatch → giu_va_canh_bao · tx=%s" % tx_id)

    elif hanh_dong == "gui_xac_thuc":
        draft = chan_cong_cu("request_verification", gd)
        if draft is None:
            request_verification(tx_id)
        note("agent: dispatch → gui_xac_thuc · tx=%s" % tx_id)

    elif hanh_dong == "hoi_lai":
        # Không gọi action tool — chỉ trả câu hỏi lại từ guard
        note("agent: dispatch → hoi_lai · tx=%s" % tx_id)

    elif hanh_dong == "chuyen_tu_van_vien":
        # Kiểm chan_cong_cu cho handoff (không cấm, nhưng pattern tốt)
        draft = chan_cong_cu("handoff_to_agent", gd)
        if draft is None:
            handoff_to_agent(
                tx_id=tx_id,
                tom_tat=kq.get("tom_tat", ""),
                suggested_action="",
            )
        note("agent: dispatch → chuyen_tu_van_vien · tx=%s" % tx_id)

    # ------------------------------------------------------------------
    # Chặn công cụ cấm bất kể luồng nào cố gọi (lớp bảo vệ rõ ràng)
    # release_transaction và lock_wallet chỉ được gọi nếu
    # chan_cong_cu trả về None — nhưng chúng thuộc CONG_CU_CAM nên
    # chan_cong_cu LUÔN chặn, trả bản nháp cho_duyet.
    # ------------------------------------------------------------------
    for ten_cam in ("release_transaction", "lock_wallet"):
        draft = chan_cong_cu(ten_cam, gd)
        # draft không phải None → đã chặn, bản nháp đã được tạo trong guard
        # Không cần làm gì thêm — guard.py đã xử lý hanh_dong cấm ở bước 3

    # ------------------------------------------------------------------
    # Bước 5: Trả kết quả
    # ------------------------------------------------------------------
    tra_loi = g.get("tra_loi") or ""
    if not tra_loi:
        # Safe fallback khi guard trả chuỗi rỗng (ví dụ chế độ giả)
        tra_loi = (
            "Mình đã nhận yêu cầu của bạn. Giao dịch vẫn đang được giữ an toàn, "
            "bạn vui lòng chờ trong giây lát."
        )
        note("agent: tra_loi rỗng — dùng fallback")

    return {"output": tra_loi}
