from typing import Any

from src.subagents.common import extract_limit
from src.tools import retail_summary, sales_by_country, top_products_by_revenue


def handle_sales_question(question: str) -> dict[str, Any]:
    q = question.lower()
    limit = extract_limit(q)

    if (
        "country" in q
        or "countries" in q
        or "market" in q
        or "markets" in q
        or "land" in q
        or "länder" in q
    ):
        return {
            "sub_agent": "sales_agent",
            "tool": "sales_by_country",
            "answer": "The Sales Agent analyzed revenue, quantity and orders by country.",
            "data": sales_by_country(limit=limit),
        }

    if (
        "product" in q
        or "products" in q
        or "item" in q
        or "items" in q
        or "highest revenue" in q
        or "top" in q
    ):
        return {
            "sub_agent": "sales_agent",
            "tool": "top_products_by_revenue",
            "answer": "The Sales Agent identified the top products by revenue.",
            "data": top_products_by_revenue(limit=limit),
        }

    return {
        "sub_agent": "sales_agent",
        "tool": "retail_summary",
        "answer": "The Sales Agent created a general retail sales summary.",
        "data": retail_summary(),
    }