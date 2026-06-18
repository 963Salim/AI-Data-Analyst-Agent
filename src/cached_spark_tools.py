import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = BASE_DIR / "data" / "cache"


def normalize_limit(limit: int = 20, max_limit: int = 100) -> int:
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 20

    return max(1, min(limit, max_limit))


def load_cached_result(filename: str) -> list[dict[str, Any]]:
    """
    Loads a precomputed Spark result from JSON.

    The JSON files are created by:
    scripts/precompute_spark_cache.py
    """
    path = CACHE_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Spark cache file not found: {path}. "
            "Run scripts/precompute_spark_cache.py first."
        )

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"Cached Spark result must be a list: {path}")

    return data


def limit_records(
    records: list[dict[str, Any]],
    limit: int,
    max_limit: int = 100,
) -> list[dict[str, Any]]:
    limit = normalize_limit(limit=limit, max_limit=max_limit)
    return records[:limit]


def spark_customer_rfm_segmentation(limit: int = 20) -> list[dict[str, Any]]:
    """
    Fast cached version of the PySpark RFM customer segmentation.
    """
    records = load_cached_result("spark_customer_rfm_segmentation.json")
    return limit_records(records, limit=limit, max_limit=100)


def spark_basket_product_pairs(
    limit: int = 20,
    min_pair_count: int = 2,
) -> list[dict[str, Any]]:
    """
    Fast cached version of the PySpark basket product-pair analysis.

    min_pair_count is accepted for compatibility with the original Spark tool.
    """
    records = load_cached_result("spark_basket_product_pairs.json")

    filtered_records = [
        record
        for record in records
        if int(record.get("shared_orders", 0)) >= int(min_pair_count)
    ]

    return limit_records(filtered_records, limit=limit, max_limit=100)


def spark_monthly_kpi_dashboard() -> list[dict[str, Any]]:
    """
    Fast cached version of the PySpark monthly KPI dashboard.
    """
    return load_cached_result("spark_monthly_kpi_dashboard.json")


def spark_country_performance_scorecard(limit: int = 20) -> list[dict[str, Any]]:
    """
    Fast cached version of the PySpark country performance scorecard.
    """
    records = load_cached_result("spark_country_performance_scorecard.json")
    return limit_records(records, limit=limit, max_limit=100)


def spark_data_quality_report() -> list[dict[str, Any]]:
    """
    Fast cached version of the PySpark extended data quality report.
    """
    return load_cached_result("spark_data_quality_report.json")