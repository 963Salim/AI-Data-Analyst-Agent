from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd


DATA_PATH = Path("data/processed/retail_clean.csv")


@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}. "
            "Run scripts/prepare_data.py first."
        )

    return pd.read_csv(DATA_PATH, low_memory=False)


def get_valid_sales(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["is_valid_sale"]].copy()


def describe_dataset() -> dict[str, Any]:
    df = load_data()

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
        "categorical_columns": df.select_dtypes(exclude="number").columns.tolist(),
    }


def check_missing_values() -> list[dict[str, Any]]:
    df = load_data()

    missing = df.isna().sum()
    result = []

    for column, count in missing.items():
        if count > 0:
            result.append({
                "column": column,
                "missing_values": int(count),
                "missing_percentage": round((count / len(df)) * 100, 2),
            })

    return result


def top_products_by_revenue(limit: int = 10) -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)

    result = (
        sales.groupby("description", as_index=False)
        .agg(
            product=("description", "first"),
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            transactions=("invoiceno", "nunique"),
        )
        .drop(columns=["description"])
        .sort_values("revenue", ascending=False)
        .head(limit)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def sales_by_country(limit: int = 10) -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)

    result = (
        sales.groupby("country", as_index=False)
        .agg(
            country=("country", "first"),
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            orders=("invoiceno", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .head(limit)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def monthly_revenue_trend() -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)

    result = (
        sales.groupby("invoice_month", as_index=False)
        .agg(
            month=("invoice_month", "first"),
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            orders=("invoiceno", "nunique"),
        )
        .drop(columns=["invoice_month"])
        .sort_values("month")
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def returns_analysis() -> dict[str, Any]:
    df = load_data()

    total_rows = len(df)
    return_rows = int(df["is_return"].sum())
    returns = df[df["is_return"]].copy()

    return {
        "total_rows": int(total_rows),
        "return_rows": return_rows,
        "return_percentage": round((return_rows / total_rows) * 100, 2),
        "total_return_quantity": int(returns["quantity"].sum()) if not returns.empty else 0,
        "total_return_value": round(float(returns["revenue"].sum()), 2) if not returns.empty else 0.0,
    }


def retail_summary() -> dict[str, Any]:
    df = load_data()
    sales = get_valid_sales(df)

    order_revenue = sales.groupby("invoiceno")["revenue"].sum()

    return {
        "rows": int(df.shape[0]),
        "valid_sales_rows": int(len(sales)),
        "unique_orders": int(sales["invoiceno"].nunique()),
        "unique_products": int(sales["stockcode"].nunique()),
        "unique_customers": int(sales[sales["customerid"] != "Unknown"]["customerid"].nunique()),
        "countries": int(sales["country"].nunique()),
        "total_revenue": round(float(sales["revenue"].sum()), 2),
        "average_order_value": round(float(order_revenue.mean()), 2),
    }