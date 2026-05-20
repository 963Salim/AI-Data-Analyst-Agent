from typing import Any

from src.tools import (
    describe_dataset,
    check_missing_values,
    top_products_by_revenue,
    sales_by_country,
    monthly_revenue_trend,
    returns_analysis,
    retail_summary,
)


def run_agent(user_question: str) -> dict[str, Any]:
    question = user_question.lower()

    if "missing" in question or "fehlende" in question or "null" in question:
        return {
            "tool": "check_missing_values",
            "answer": "I checked the dataset for missing values.",
            "data": check_missing_values(),
        }

    if "top product" in question or "products" in question or "produkt" in question:
        return {
            "tool": "top_products_by_revenue",
            "answer": "I identified the top products by revenue.",
            "data": top_products_by_revenue(limit=10),
        }

    if "country" in question or "länder" in question or "land" in question:
        return {
            "tool": "sales_by_country",
            "answer": "I summarized sales by country.",
            "data": sales_by_country(limit=10),
        }

    if "month" in question or "monthly" in question or "monat" in question:
        return {
            "tool": "monthly_revenue_trend",
            "answer": "I calculated the monthly revenue trend.",
            "data": monthly_revenue_trend(),
        }

    if "return" in question or "rückgabe" in question or "storno" in question:
        return {
            "tool": "returns_analysis",
            "answer": "I analyzed returns in the dataset.",
            "data": returns_analysis(),
        }

    if "describe" in question or "overview" in question or "übersicht" in question:
        return {
            "tool": "describe_dataset",
            "answer": "I created a structural overview of the dataset.",
            "data": describe_dataset(),
        }

    return {
        "tool": "retail_summary",
        "answer": "I created a general retail summary.",
        "data": retail_summary(),
    }