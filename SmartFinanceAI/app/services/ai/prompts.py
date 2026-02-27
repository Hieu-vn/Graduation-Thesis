"""
Prompts Service - System Prompts & Templates for AI Chatbot

Defines system prompts for each intent type (FR25, FR26, FR27)
and utility functions to build context-enriched prompts.
"""
import json
from typing import Any, Dict


# ============================================================
# SYSTEM PROMPTS
# ============================================================

SYSTEM_PROMPT_BASE = """Bạn là chuyên gia tư vấn tài chính cá nhân AI của hệ thống SmartFinance.
Quy tắc:
- Luôn trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu.
- Sử dụng đơn vị tiền tệ VND, định dạng số có dấu chấm phân cách hàng nghìn (ví dụ: 1.500.000đ).
- CHỈ trả lời dựa trên dữ liệu tài chính thực tế được cung cấp, KHÔNG bịa số liệu.
- Nếu không có đủ dữ liệu, hãy nói rõ và yêu cầu người dùng cung cấp thêm.
- Giữ câu trả lời ngắn gọn, có cấu trúc rõ ràng (dùng bullet points khi cần).
"""

SYSTEM_PROMPT_LOOKUP = SYSTEM_PROMPT_BASE + """
Bạn đang ở chế độ TRA CỨU THÔNG TIN (FR25).
Nhiệm vụ: Trả lời câu hỏi về số liệu tài chính cá nhân dựa trên dữ liệu được cung cấp.
- Cung cấp số liệu chính xác từ dữ liệu.
- Nếu hỏi về tổng chi, tổng thu, số dư: trả lời thẳng với con số cụ thể.
- Nếu hỏi về giao dịch cụ thể: liệt kê chi tiết.
"""

SYSTEM_PROMPT_TREND = SYSTEM_PROMPT_BASE + """
Bạn đang ở chế độ PHÂN TÍCH XU HƯỚNG (FR26).
Nhiệm vụ: Phân tích và so sánh xu hướng chi tiêu giữa các kỳ.
- So sánh tổng chi tiêu giữa kỳ hiện tại và kỳ trước.
- Chỉ ra danh mục tăng/giảm mạnh nhất với % thay đổi.
- Nhận xét xu hướng tổng thể (tăng/giảm/ổn định).
"""

SYSTEM_PROMPT_ADVICE = SYSTEM_PROMPT_BASE + """
Bạn đang ở chế độ TƯ VẤN TÀI CHÍNH (FR27).
Nhiệm vụ: Đưa ra lời khuyên tài chính cá nhân hóa.
- Phân tích tình hình thu chi, ngân sách, tiết kiệm.
- Chỉ ra danh mục chi tiêu quá mức hoặc có thể cắt giảm.
- Đề xuất 2-3 hành động cụ thể để cải thiện tài chính.
- Tính toán tỷ lệ tiết kiệm và so sánh với mục tiêu thông thường (≥20%).
"""

SYSTEM_PROMPT_GENERAL = SYSTEM_PROMPT_BASE + """
Nhiệm vụ: Trả lời câu hỏi chung liên quan đến tài chính cá nhân.
Nếu câu hỏi liên quan đến số liệu cá nhân, hãy dựa trên dữ liệu được cung cấp.
Nếu câu hỏi là kiến thức chung về tài chính, hãy trả lời dựa trên hiểu biết của bạn.
"""

# ============================================================
# Intent classifier prompt
# ============================================================

INTENT_CLASSIFICATION_PROMPT = """Phân tích câu hỏi sau và trả về JSON (KHÔNG markdown, KHÔNG giải thích):

Câu hỏi: "{query}"

Trả về ĐÚNG định dạng JSON sau:
{{"intent": "<lookup|trend|advice|general>", "entities": {{"start_date": "<YYYY-MM-DD hoặc null>", "end_date": "<YYYY-MM-DD hoặc null>", "category": "<tên danh mục hoặc null>", "account": "<tên ví hoặc null>"}}}}

Quy tắc phân loại intent:
- "lookup": Hỏi số liệu cụ thể (tổng chi, số dư, giao dịch, thu nhập...)
- "trend": So sánh, xu hướng (so với tháng trước, tăng giảm, biến động...)
- "advice": Xin lời khuyên (nên cắt giảm, tiết kiệm, đầu tư, cải thiện...)
- "general": Câu hỏi chung, chào hỏi, không liên quan trực tiếp đến dữ liệu cá nhân

Quy tắc trích xuất thời gian (ngày hôm nay: {today}):
- "tháng này" → start_date = ngày đầu tháng hiện tại, end_date = hôm nay
- "tháng trước" → start_date/end_date = tháng trước
- "tuần này" → 7 ngày gần nhất
- "năm nay" → từ 01/01 đến hôm nay
- Nếu không rõ → null (hệ thống sẽ dùng tháng hiện tại)
"""


# ============================================================
# Context formatting
# ============================================================

def get_system_prompt(intent: str) -> str:
    """Get the appropriate system prompt based on intent."""
    prompts = {
        "lookup": SYSTEM_PROMPT_LOOKUP,
        "trend": SYSTEM_PROMPT_TREND,
        "advice": SYSTEM_PROMPT_ADVICE,
        "general": SYSTEM_PROMPT_GENERAL,
    }
    return prompts.get(intent, SYSTEM_PROMPT_GENERAL)


def format_context(context: Dict[str, Any]) -> str:
    """Format retrieved financial data into a readable string for the LLM."""
    parts = []

    if "spending" in context:
        s = context["spending"]
        parts.append(f"📊 CHI TIÊU ({s['start_date']} → {s['end_date']}):")
        parts.append(f"  Tổng chi: {s['total_spending']:,.0f}đ ({s['transaction_count']} giao dịch)")
        for cat in s["categories"]:
            parts.append(f"  - {cat['category']}: {cat['amount']:,.0f}đ ({cat['count']} GD)")

    if "income" in context:
        i = context["income"]
        parts.append(f"\n💰 THU NHẬP ({i['start_date']} → {i['end_date']}):")
        parts.append(f"  Tổng thu: {i['total_income']:,.0f}đ")
        for cat in i["categories"]:
            parts.append(f"  - {cat['category']}: {cat['amount']:,.0f}đ")

    if "balances" in context:
        parts.append("\n🏦 SỐ DƯ CÁC VÍ:")
        for acc in context["balances"]:
            parts.append(f"  - {acc['name']} ({acc['type']}): {acc['balance']:,.0f} {acc['currency']}")

    if "budgets" in context:
        parts.append("\n📋 NGÂN SÁCH:")
        for b in context["budgets"]:
            status = "⚠️ VƯỢT" if b["usage_percent"] > 100 else "✅"
            parts.append(
                f"  - {b['category']}: {b['actual_spending']:,.0f}đ / {b['budget_amount']:,.0f}đ "
                f"({b['usage_percent']}%) {status}"
            )

    if "comparison" in context:
        c = context["comparison"]
        parts.append(f"\n📈 SO SÁNH CHI TIÊU:")
        parts.append(f"  Kỳ hiện tại: {c['current_period']['total']:,.0f}đ")
        parts.append(f"  Kỳ trước: {c['previous_period']['total']:,.0f}đ")
        parts.append(f"  Thay đổi: {c['total_change']:+,.0f}đ ({c['total_change_percent']:+.1f}%)")
        parts.append("  Chi tiết theo danh mục:")
        for cat in c["by_category"][:5]:
            parts.append(
                f"    - {cat['category']}: {cat['current_amount']:,.0f}đ → "
                f"{cat['change_percent']:+.1f}%"
            )

    if "recent_transactions" in context:
        parts.append(f"\n📝 GIAO DỊCH GẦN ĐÂY:")
        for t in context["recent_transactions"][:10]:
            emoji = "🔴" if t["type"] == "expense" else "🟢"
            parts.append(
                f"  {emoji} {t['date']} | {t['description']} | "
                f"{t['amount']:,.0f}đ | {t['category']}"
            )

    if "semantic_matches" in context and context["semantic_matches"]:
        parts.append(f"\n🔍 GIAO DỊCH LIÊN QUAN (tìm kiếm ngữ nghĩa):")
        for m in context["semantic_matches"]:
            meta = m["metadata"]
            parts.append(
                f"  - {m['document']} | {meta.get('amount', 0):,.0f}đ | {meta.get('date', '')}"
            )

    return "\n".join(parts)


def build_user_prompt(query: str, context: Dict[str, Any]) -> str:
    """Build the complete user prompt with formatted context."""
    context_str = format_context(context)

    return f"""DỮ LIỆU TÀI CHÍNH CỦA NGƯỜI DÙNG:
{context_str}

CÂU HỎI CỦA NGƯỜI DÙNG:
{query}

Hãy trả lời dựa trên dữ liệu trên."""
