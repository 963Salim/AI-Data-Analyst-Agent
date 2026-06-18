from functools import lru_cache

from pyspark.sql import SparkSession


@lru_cache(maxsize=1)
def get_spark_session() -> SparkSession:
    """
    Creates one reusable local SparkSession for the project.

    The session is cached so the app does not create a new SparkSession
    for every user question.
    """
    spark = (
        SparkSession.builder
        .appName("AI Data Analyst Agent - PySpark Analytics")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")
    return spark