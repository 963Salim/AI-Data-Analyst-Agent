from typing import Any

from src.subagents.common import (
    extract_country_from_question,
    extract_limit_from_question,
)


def route_trend_tool(question: str) -> tuple[str, dict[str, Any]]:
    """
    Trend sub-agent:
    Handles monthly and time-based development questions.
    """
    q = question.lower()
    country = extract_country_from_question(question)

    if "average order value" in q or "aov" in q:
        return "monthly_average_order_value", {}

    if "order" in q:
        return "monthly_orders_trend", {}

    if "country" in q or country:
        return "revenue_by_country_and_month", {
            "country": country,
            "limit": extract_limit_from_question(
                question,
                default=100,
                max_limit=500,
            ),
        }

    return "monthly_revenue_trend", {}