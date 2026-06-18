from pathlib import Path
from typing import Any

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from src.spark_session import get_spark_session


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "retail_clean.csv"


REQUIRED_COLUMNS = {
    "invoiceno",
    "stockcode",
    "description",
    "quantity",
    "invoicedate",
    "unitprice",
    "customerid",
    "country",
    "is_return",
    "revenue",
    "invoice_month",
    "invoice_date",
    "is_valid_sale",
}


def row_to_dict(row: Any) -> dict[str, Any]:
    """
    Converts a Spark Row into a normal Python dictionary.
    Date and timestamp values are converted to strings so FastAPI can return them as JSON.
    """
    record = row.asDict()

    for key, value in record.items():
        if hasattr(value, "isoformat"):
            record[key] = value.isoformat()

    return record


def collect_records(df: DataFrame, limit: int = 50) -> list[dict[str, Any]]:
    """
    Converts a Spark DataFrame into a list of dictionaries for the FastAPI frontend.
    Only small aggregated results should be collected to the driver.
    """
    return [row_to_dict(row) for row in df.limit(limit).collect()]


def normalize_limit(limit: int = 20, max_limit: int = 100) -> int:
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 20

    return max(1, min(limit, max_limit))


def normalize_boolean_column(column_name: str) -> F.Column:
    """
    Handles boolean values stored as True/False, true/false, 1/0 or yes/no.
    """
    return (
        F.lower(F.col(column_name).cast("string"))
        .isin("true", "1", "yes", "y")
    )


def load_spark_data() -> DataFrame:
    """
    Loads the processed retail dataset as a Spark DataFrame and standardizes types.

    The file is created by the existing pandas pipeline:
    data/processed/retail_clean.csv
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}. "
            "Run scripts/prepare_data.py first."
        )

    spark = get_spark_session()

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .option("quote", '"')
        .option("escape", '"')
        .csv(str(DATA_PATH))
    )

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(
            "The processed dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    df = (
        df.withColumn("invoiceno", F.col("invoiceno").cast("string"))
        .withColumn("stockcode", F.upper(F.trim(F.col("stockcode").cast("string"))))
        .withColumn("description", F.trim(F.col("description").cast("string")))
        .withColumn("customerid", F.trim(F.col("customerid").cast("string")))
        .withColumn("country", F.trim(F.col("country").cast("string")))
        .withColumn("quantity", F.col("quantity").cast("double"))
        .withColumn("unitprice", F.col("unitprice").cast("double"))
        .withColumn("revenue", F.col("revenue").cast("double"))
        .withColumn("invoicedate", F.to_timestamp("invoicedate"))
        .withColumn("invoice_date", F.to_date("invoice_date"))
        .withColumn("invoice_month", F.col("invoice_month").cast("string"))
        .withColumn("is_return", normalize_boolean_column("is_return"))
        .withColumn("is_valid_sale", normalize_boolean_column("is_valid_sale"))
    )

    return df.cache()


def get_valid_sales(df: DataFrame) -> DataFrame:
    return df.filter(F.col("is_valid_sale") == True)


def spark_customer_rfm_segmentation(limit: int = 20) -> list[dict[str, Any]]:
    """
    Advanced Spark analysis:
    Creates customer segments using RFM logic.

    RFM means:
    - Recency: how recently the customer purchased
    - Frequency: how often the customer purchased
    - Monetary: how much revenue the customer generated
    """
    limit = normalize_limit(limit)

    df = load_spark_data()
    sales = (
        get_valid_sales(df)
        .filter(F.col("customerid").isNotNull())
        .filter(F.col("customerid") != "Unknown")
    )

    max_invoice_date = sales.select(F.max("invoice_date")).first()[0]

    if max_invoice_date is None:
        return []

    reference_date = F.date_add(F.lit(max_invoice_date), 1)

    rfm = (
        sales.groupBy("customerid")
        .agg(
            F.max("invoice_date").alias("last_purchase_date"),
            F.countDistinct("invoiceno").alias("frequency"),
            F.round(F.sum("revenue"), 2).alias("monetary_value"),
            F.round(F.sum("quantity"), 2).alias("total_quantity"),
        )
        .withColumn(
            "recency_days",
            F.datediff(reference_date, F.col("last_purchase_date")),
        )
    )

    recency_window = Window.orderBy(F.col("recency_days").asc())
    frequency_window = Window.orderBy(F.col("frequency").asc())
    monetary_window = Window.orderBy(F.col("monetary_value").asc())

    rfm = (
        rfm.withColumn("recency_score", F.lit(6) - F.ntile(5).over(recency_window))
        .withColumn("frequency_score", F.ntile(5).over(frequency_window))
        .withColumn("monetary_score", F.ntile(5).over(monetary_window))
        .withColumn(
            "rfm_score",
            F.col("recency_score") + F.col("frequency_score") + F.col("monetary_score"),
        )
        .withColumn(
            "customer_segment",
            F.when(F.col("rfm_score") >= 13, "Champions")
            .when(
                (F.col("frequency_score") >= 4) & (F.col("monetary_score") >= 4),
                "High Value Customers",
            )
            .when(
                (F.col("recency_score") <= 2) & (F.col("monetary_score") >= 3),
                "At Risk Customers",
            )
            .when(F.col("recency_score") >= 4, "Recent Active Customers")
            .otherwise("Standard Customers"),
        )
        .orderBy(F.desc("rfm_score"), F.desc("monetary_value"))
    )

    return collect_records(rfm, limit=limit)


def spark_basket_product_pairs(
    limit: int = 20,
    min_pair_count: int = 2,
) -> list[dict[str, Any]]:
    """
    Advanced Spark analysis:
    Identifies products that are often bought together in the same invoice.

    This is useful for basket analysis, cross-selling ideas and product bundling.
    """
    limit = normalize_limit(limit)

    df = load_spark_data()
    sales = get_valid_sales(df)

    items = (
        sales.select("invoiceno", "stockcode", "description")
        .filter(F.col("invoiceno").isNotNull())
        .filter(F.col("stockcode").isNotNull())
        .filter(F.col("description").isNotNull())
        .dropDuplicates(["invoiceno", "stockcode"])
    )

    left_items = items.alias("left_items")
    right_items = items.alias("right_items")

    product_pairs = (
        left_items.join(
            right_items,
            (F.col("left_items.invoiceno") == F.col("right_items.invoiceno"))
            & (F.col("left_items.stockcode") < F.col("right_items.stockcode")),
            "inner",
        )
        .groupBy(
            F.col("left_items.stockcode").alias("product_a_code"),
            F.col("left_items.description").alias("product_a"),
            F.col("right_items.stockcode").alias("product_b_code"),
            F.col("right_items.description").alias("product_b"),
        )
        .agg(
            F.countDistinct(F.col("left_items.invoiceno")).alias("shared_orders")
        )
        .filter(F.col("shared_orders") >= min_pair_count)
        .orderBy(F.desc("shared_orders"))
    )

    return collect_records(product_pairs, limit=limit)


def spark_monthly_kpi_dashboard() -> list[dict[str, Any]]:
    """
    Advanced Spark analysis:
    Creates a monthly KPI table with multiple business metrics.

    This is broader than a simple monthly revenue trend because it combines:
    revenue, orders, customers, quantity, AOV and return metrics.
    """
    df = load_spark_data()

    sales = get_valid_sales(df)

    monthly_sales = (
        sales.groupBy("invoice_month")
        .agg(
            F.round(F.sum("revenue"), 2).alias("revenue"),
            F.round(F.sum("quantity"), 2).alias("quantity"),
            F.countDistinct("invoiceno").alias("orders"),
            F.countDistinct(
                F.when(F.col("customerid") != "Unknown", F.col("customerid"))
            ).alias("known_customers"),
        )
    )

    monthly_returns = (
        df.groupBy("invoice_month")
        .agg(
            F.count("*").alias("total_rows"),
            F.sum(F.when(F.col("is_return") == True, 1).otherwise(0)).alias("return_rows"),
            F.round(
                F.sum(
                    F.when(F.col("is_return") == True, F.abs(F.col("revenue")))
                    .otherwise(0)
                ),
                2,
            ).alias("return_value"),
        )
    )

    dashboard = (
        monthly_sales.join(monthly_returns, on="invoice_month", how="left")
        .fillna({"return_rows": 0, "return_value": 0.0})
        .withColumn(
            "average_order_value",
            F.round(F.col("revenue") / F.col("orders"), 2),
        )
        .withColumn(
            "return_rate_percentage",
            F.round((F.col("return_rows") / F.col("total_rows")) * 100, 2),
        )
        .withColumnRenamed("invoice_month", "month")
        .orderBy("month")
    )

    return collect_records(dashboard, limit=500)


def spark_country_performance_scorecard(limit: int = 20) -> list[dict[str, Any]]:
    """
    Advanced Spark analysis:
    Creates a country-level performance scorecard.

    This is more advanced than simple sales by country because it combines:
    revenue, orders, customers, AOV, return rate and ranks.
    """
    limit = normalize_limit(limit)

    df = load_spark_data()
    sales = get_valid_sales(df)

    country_sales = (
        sales.groupBy("country")
        .agg(
            F.round(F.sum("revenue"), 2).alias("revenue"),
            F.round(F.sum("quantity"), 2).alias("quantity"),
            F.countDistinct("invoiceno").alias("orders"),
            F.countDistinct(
                F.when(F.col("customerid") != "Unknown", F.col("customerid"))
            ).alias("known_customers"),
        )
    )

    country_returns = (
        df.groupBy("country")
        .agg(
            F.count("*").alias("total_rows"),
            F.sum(F.when(F.col("is_return") == True, 1).otherwise(0)).alias("return_rows"),
            F.round(
                F.sum(
                    F.when(F.col("is_return") == True, F.abs(F.col("revenue")))
                    .otherwise(0)
                ),
                2,
            ).alias("return_value"),
        )
    )

    revenue_rank_window = Window.orderBy(F.desc("revenue"))
    return_rank_window = Window.orderBy(F.asc("return_rate_percentage"))

    scorecard = (
        country_sales.join(country_returns, on="country", how="left")
        .fillna({"return_rows": 0, "return_value": 0.0})
        .withColumn(
            "average_order_value",
            F.round(F.col("revenue") / F.col("orders"), 2),
        )
        .withColumn(
            "return_rate_percentage",
            F.round((F.col("return_rows") / F.col("total_rows")) * 100, 2),
        )
        .withColumn("revenue_rank", F.dense_rank().over(revenue_rank_window))
        .withColumn("return_rate_rank", F.dense_rank().over(return_rank_window))
        .withColumn(
            "performance_score",
            F.col("revenue_rank") + F.col("return_rate_rank"),
        )
        .orderBy(F.desc("revenue"))
    )

    return collect_records(scorecard, limit=limit)


def spark_data_quality_report() -> list[dict[str, Any]]:
    """
    Advanced Spark analysis:
    Creates a fuller data quality report.

    It checks:
    - missing or empty values by column
    - distinct values by column
    - invalid quantities
    - invalid prices
    - invalid dates
    - unknown customer rows
    - duplicate full rows
    """
    df = load_spark_data()

    total_rows = df.count()
    report: list[dict[str, Any]] = []

    for column in df.columns:
        missing_or_empty_count = df.filter(
            F.col(column).isNull()
            | (F.lower(F.trim(F.col(column).cast("string"))).isin("", "nan", "none", "null"))
        ).count()

        distinct_count = df.select(column).distinct().count()

        report.append(
            {
                "check_type": "column_quality",
                "column": column,
                "metric": "missing_or_empty_values",
                "value": int(missing_or_empty_count),
                "percentage": round((missing_or_empty_count / total_rows) * 100, 2)
                if total_rows
                else 0.0,
            }
        )

        report.append(
            {
                "check_type": "column_quality",
                "column": column,
                "metric": "distinct_values",
                "value": int(distinct_count),
                "percentage": None,
            }
        )

    invalid_quantity_rows = df.filter(F.col("quantity").isNull()).count()
    invalid_price_rows = df.filter(F.col("unitprice").isNull()).count()
    invalid_date_rows = df.filter(F.col("invoice_date").isNull()).count()
    unknown_customer_rows = df.filter(F.col("customerid") == "Unknown").count()
    duplicate_full_rows = total_rows - df.dropDuplicates().count()

    dataset_checks = [
        ("invalid_quantity_rows", invalid_quantity_rows),
        ("invalid_price_rows", invalid_price_rows),
        ("invalid_date_rows", invalid_date_rows),
        ("unknown_customer_rows", unknown_customer_rows),
        ("duplicate_full_rows", duplicate_full_rows),
    ]

    for metric, value in dataset_checks:
        report.append(
            {
                "check_type": "dataset_quality",
                "column": "all_columns",
                "metric": metric,
                "value": int(value),
                "percentage": round((value / total_rows) * 100, 2)
                if total_rows
                else 0.0,
            }
        )

    return report