import sys
from pathlib import Path
from pprint import pprint


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))


from src.spark_session import get_spark_session
from src.spark_tools import (
    spark_basket_product_pairs,
    spark_country_performance_scorecard,
    spark_customer_rfm_segmentation,
    spark_data_quality_report,
    spark_monthly_kpi_dashboard,
)


def print_section(title: str) -> None:
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def main() -> None:
    print_section("Spark Customer RFM Segmentation")
    pprint(spark_customer_rfm_segmentation(limit=5))

    print_section("Spark Basket Product Pairs")
    pprint(spark_basket_product_pairs(limit=5))

    print_section("Spark Monthly KPI Dashboard")
    pprint(spark_monthly_kpi_dashboard()[:5])

    print_section("Spark Country Performance Scorecard")
    pprint(spark_country_performance_scorecard(limit=5))

    print_section("Spark Data Quality Report")
    pprint(spark_data_quality_report()[:10])

    spark = get_spark_session()
    spark.stop()


if __name__ == "__main__":
    main()