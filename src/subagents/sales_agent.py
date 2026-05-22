from typing import Any

from src.subagents.common import extract_limit
from src.tools import retail_summary, sales_by_country, top_products_by_revenue
from src.spark_tools import sales_by_country_spark, top_products_by_revenue_spark


def handle_sales_question(question: str, engine: str = "pandas") -> dict[str, Any]:
    q = question.lower()
    limit = extract_limit(q)
    use_spark = engine == "spark"

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
            "tool": "sales_by_country_spark" if use_spark else "sales_by_country",
            "answer": (
                "The Sales Agent analyzed revenue, quantity and orders by country "
                f"using {'PySpark' if use_spark else 'pandas'}."
            ),
            "data": sales_by_country_spark(limit=limit) if use_spark else sales_by_country(limit=limit),
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
            "tool": "top_products_by_revenue_spark" if use_spark else "top_products_by_revenue",
            "answer": (
                "The Sales Agent identified the top products by revenue "
                f"using {'PySpark' if use_spark else 'pandas'}."
            ),
            "data": top_products_by_revenue_spark(limit=limit) if use_spark else top_products_by_revenue(limit=limit),
        }

    return {
        "sub_agent": "sales_agent",
        "tool": "retail_summary",
        "answer": "The Sales Agent created a general retail sales summary using pandas.",
        "data": retail_summary(),
    }