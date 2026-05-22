import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.tools import (
    sales_by_country,
    top_products_by_revenue,
    monthly_revenue_trend,
)

from src.spark_tools import (
    sales_by_country_spark,
    top_products_by_revenue_spark,
    monthly_revenue_trend_spark,
)


if __name__ == "__main__":
    print("Pandas sales by country:")
    print(sales_by_country(limit=5))

    print("\nSpark sales by country:")
    print(sales_by_country_spark(limit=5))

    print("\nPandas top products:")
    print(top_products_by_revenue(limit=5))

    print("\nSpark top products:")
    print(top_products_by_revenue_spark(limit=5))
    
    print("\nPandas monthly revenue trend:")
print(monthly_revenue_trend()[:5])

print("\nSpark monthly revenue trend:")
print(monthly_revenue_trend_spark()[:5])

print("\nPandas monthly revenue trend:")
print(monthly_revenue_trend()[:5])

print("\nSpark monthly revenue trend:")
print(monthly_revenue_trend_spark()[:5])