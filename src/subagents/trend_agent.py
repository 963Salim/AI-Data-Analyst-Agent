from typing import Any

from src.tools import monthly_revenue_trend


def handle_trend_question(question: str) -> dict[str, Any]:
    return {
        "sub_agent": "trend_agent",
        "tool": "monthly_revenue_trend",
        "answer": "The Trend Agent analyzed the monthly revenue development.",
        "data": monthly_revenue_trend(),
    }