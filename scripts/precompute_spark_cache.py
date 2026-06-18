import json
import sys
import traceback
from pathlib import Path
from typing import Any, Callable


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

CACHE_DIR = BASE_DIR / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

from src.spark_session import get_spark_session
from src.spark_tools import (
    spark_basket_product_pairs,
    spark_country_performance_scorecard,
    spark_customer_rfm_segmentation,
    spark_data_quality_report,
    spark_monthly_kpi_dashboard,
)


def save_json(filename: str, data: Any) -> None:
    path = CACHE_DIR / filename

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print(f"Saved: {path}")


def run_cache_job(
    label: str,
    filename: str,
    function: Callable[[], Any],
) -> None:
    print("\n" + "=" * 80)
    print(f"Creating cache: {label}")
    print("=" * 80)

    path = CACHE_DIR / filename

    try:
        data = function()
        save_json(filename, data)
        print(f"Done: {filename}")

    except Exception:
        print(f"FAILED: {label}")
        print(f"Target file: {path}")
        traceback.print_exc()


def main() -> None:
    print("Precomputing Spark cache files...")

    run_cache_job(
        label="RFM customer segmentation",
        filename="spark_customer_rfm_segmentation.json",
        function=lambda: spark_customer_rfm_segmentation(limit=100),
    )

    run_cache_job(
        label="Monthly KPI dashboard",
        filename="spark_monthly_kpi_dashboard.json",
        function=spark_monthly_kpi_dashboard,
    )

    run_cache_job(
        label="Country performance scorecard",
        filename="spark_country_performance_scorecard.json",
        function=lambda: spark_country_performance_scorecard(limit=100),
    )

    run_cache_job(
        label="Spark data quality report",
        filename="spark_data_quality_report.json",
        function=spark_data_quality_report,
    )

    # Basket analysis is usually the slowest job.
    # It is placed last so the other cache files are created first.
    run_cache_job(
        label="Basket product pairs",
        filename="spark_basket_product_pairs.json",
        function=lambda: spark_basket_product_pairs(limit=100, min_pair_count=2),
    )

    spark = get_spark_session()
    spark.stop()

    print("\nSpark cache precomputation finished.")
    print(f"Cache directory: {CACHE_DIR}")


if __name__ == "__main__":
    main()