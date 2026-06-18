from typing import Any

from src.subagents.common import (
    extract_country_from_question,
    extract_limit_from_question,
)


def route_sales_tool(question: str) -> tuple[str, dict[str, Any]]:
    """
    Sales sub-agent:
    Handles revenue, country, product, customer and AOV questions.
    """
    q = question.lower()
    limit = extract_limit_from_question(question, default=10, max_limit=50)
    country = extract_country_from_question(question)

    if "customer" in q:
        return "top_customers_by_revenue", {"limit": limit}

    if "product" in q or "item" in q or "sku" in q:
        if country:
            return "top_products_by_country", {
                "country": country,
                "limit": limit,
            }

        return "top_products_by_revenue", {"limit": limit}

    if "average order value" in q or "aov" in q:
        return "average_order_value_by_country", {"limit": limit}

    if "country" in q or "market" in q:
        return "sales_by_country", {"limit": limit}

    return "sales_by_country", {"limit": limit}