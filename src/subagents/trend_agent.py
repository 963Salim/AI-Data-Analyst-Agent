from typing import Any

from src.tools import monthly_revenue_trend
from src.spark_tools import monthly_revenue_trend_spark


def handle_trend_question(question: str, engine: str = "pandas") -> dict[str, Any]:
    use_spark = engine == "spark"

    return {
        "sub_agent": "trend_agent",
        "tool": "monthly_revenue_trend_spark" if use_spark else "monthly_revenue_trend",
        "answer": (
            "The Trend Agent analyzed the monthly revenue development "
            f"using {'PySpark' if use_spark else 'pandas'}."
        ),
        "data": monthly_revenue_trend_spark() if use_spark else monthly_revenue_trend(),
    }