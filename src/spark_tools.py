from functools import lru_cache
from pathlib import Path
from typing import Any

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


DATA_PATH = Path("data/processed/retail_clean.csv")


@lru_cache(maxsize=1)
def get_spark() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("AI Retail Data Analyst Agent")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark


@lru_cache(maxsize=1)
def load_spark_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}. "
            "Run scripts/prepare_data.py first."
        )

    spark = get_spark()

    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(DATA_PATH))
    )


def get_valid_sales_spark():
    df = load_spark_data()

    return df.filter(
        (F.col("is_valid_sale") == True)
        | (F.lower(F.col("is_valid_sale").cast("string")) == "true")
    )


def sales_by_country_spark(limit: int = 10) -> list[dict[str, Any]]:
    sales = get_valid_sales_spark()

    result = (
        sales.groupBy("country")
        .agg(
            F.round(F.sum("revenue"), 2).alias("revenue"),
            F.sum("quantity").alias("quantity"),
            F.countDistinct("invoiceno").alias("orders"),
        )
        .orderBy(F.col("revenue").desc())
        .limit(limit)
    )

    return [row.asDict() for row in result.collect()]


def top_products_by_revenue_spark(limit: int = 10) -> list[dict[str, Any]]:
    sales = get_valid_sales_spark()

    result = (
        sales.groupBy("description")
        .agg(
            F.first("description").alias("product"),
            F.round(F.sum("revenue"), 2).alias("revenue"),
            F.sum("quantity").alias("quantity"),
            F.countDistinct("invoiceno").alias("transactions"),
        )
        .select("product", "revenue", "quantity", "transactions")
        .orderBy(F.col("revenue").desc())
        .limit(limit)
    )

    return [row.asDict() for row in result.collect()]


def monthly_revenue_trend_spark() -> list[dict[str, Any]]:
    sales = get_valid_sales_spark()

    result = (
        sales.groupBy("invoice_month")
        .agg(
            F.round(F.sum("revenue"), 2).alias("revenue"),
            F.sum("quantity").alias("quantity"),
            F.countDistinct("invoiceno").alias("orders"),
        )
        .withColumn(
            "month",
            F.substring(F.col("invoice_month").cast("string"), 1, 7),
        )
        .select("month", "revenue", "quantity", "orders")
        .orderBy("month")
    )

    return [row.asDict() for row in result.collect()]