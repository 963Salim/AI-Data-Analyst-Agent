from typing import Any

from src.subagents.common import extract_limit_from_question


def route_returns_tool(question: str) -> tuple[str, dict[str, Any]]:
    """
    Returns sub-agent:
    Handles returns, cancellations and return-rate questions.
    """
    q = question.lower()
    limit = extract_limit_from_question(question, default=10, max_limit=50)

    if "country" in q:
        return "return_rate_by_country", {"limit": limit}

    if "product" in q or "item" in q or "sku" in q:
        return "return_rate_by_product", {"limit": limit}

    return "returns_analysis", {}