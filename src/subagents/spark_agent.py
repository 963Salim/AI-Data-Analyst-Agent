from typing import Any

from src.subagents.common import extract_limit_from_question


def route_spark_tool(question: str) -> tuple[str, dict[str, Any]]:
    """
    Spark sub-agent:
    Handles advanced cached PySpark analytics.
    """
    q = question.lower()
    limit = extract_limit_from_question(question, default=20, max_limit=100)

    if (
        "rfm" in q
        or "segment" in q
        or "segmentation" in q
        or "champion" in q
        or "champions" in q
    ):
        return "spark_customer_rfm_segmentation", {"limit": limit}

    if (
        "basket" in q
        or "market basket" in q
        or "bought together" in q
        or "often bought" in q
        or "product pair" in q
        or "product pairs" in q
        or "together" in q
    ):
        return "spark_basket_product_pairs", {"limit": limit}

    if (
        "scorecard" in q
        or "country performance" in q
        or "compare countries" in q
        or "aov and return rate" in q
        or "revenue, aov" in q
    ):
        return "spark_country_performance_scorecard", {"limit": limit}

    if (
        "kpi dashboard" in q
        or "advanced monthly" in q
        or "monthly kpi" in q
    ):
        return "spark_monthly_kpi_dashboard", {}

    if (
        "validation" in q
        or "data quality" in q
        or "quality report" in q
        or "extended" in q
        or "full data quality" in q
    ):
        return "spark_data_quality_report", {}

    return "spark_customer_rfm_segmentation", {"limit": limit}