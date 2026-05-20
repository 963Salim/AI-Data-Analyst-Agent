import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.tools import (
    describe_dataset,
    check_missing_values,
    top_products_by_revenue,
    sales_by_country,
    monthly_revenue_trend,
    returns_analysis,
    retail_summary,
)


def print_section(title, data):
    print(f"\n--- {title} ---")
    print(data)


if __name__ == "__main__":
    print_section("Dataset description", describe_dataset())
    print_section("Missing values", check_missing_values())
    print_section("Retail summary", retail_summary())
    print_section("Top products by revenue", top_products_by_revenue(limit=5))
    print_section("Sales by country", sales_by_country(limit=5))
    print_section("Monthly revenue trend", monthly_revenue_trend()[:5])
    print_section("Returns analysis", returns_analysis())