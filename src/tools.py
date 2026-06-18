from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd


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


COLUMN_ALIASES = {
    "invoice": "invoiceno",
    "invoice_no": "invoiceno",
    "order": "invoiceno",
    "orders": "invoiceno",
    "transaction": "invoiceno",
    "transactions": "invoiceno",
    "product": "description",
    "products": "description",
    "item": "description",
    "items": "description",
    "sku": "stockcode",
    "stock_code": "stockcode",
    "customer": "customerid",
    "customers": "customerid",
    "country_name": "country",
    "market": "country",
    "markets": "country",
    "month": "invoice_month",
    "date": "invoice_date",
    "price": "unitprice",
    "sales": "revenue",
    "turnover": "revenue",
}


ALLOWED_GROUP_COLUMNS = {
    "invoiceno",
    "stockcode",
    "description",
    "customerid",
    "country",
    "invoice_month",
    "invoice_date",
    "is_return",
    "is_valid_sale",
}


ALLOWED_METRIC_COLUMNS = {
    "revenue",
    "quantity",
    "unitprice",
    "invoiceno",
    "stockcode",
    "customerid",
}


ALLOWED_AGGREGATIONS = {
    "sum",
    "mean",
    "median",
    "min",
    "max",
    "count",
    "nunique",
}


def normalize_column_name(column: str) -> str:
    cleaned = column.strip().lower()
    return COLUMN_ALIASES.get(cleaned, cleaned)


def normalize_limit(limit: int = 10, max_limit: int = 100) -> int:
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 10

    return max(1, min(limit, max_limit))


def validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            "The processed dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )


def normalize_boolean_column(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series

    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .isin({"true", "1", "yes", "y"})
    )


@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATA_PATH}. "
            "Run scripts/prepare_data.py first."
        )

    df = pd.read_csv(DATA_PATH, low_memory=False)

    validate_required_columns(df)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["unitprice"] = pd.to_numeric(df["unitprice"], errors="coerce").fillna(0)
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0)

    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["invoice_month"] = df["invoice_month"].astype(str)

    df["is_return"] = normalize_boolean_column(df["is_return"])
    df["is_valid_sale"] = normalize_boolean_column(df["is_valid_sale"])

    df["invoiceno"] = df["invoiceno"].astype(str)
    df["stockcode"] = df["stockcode"].astype(str)
    df["description"] = df["description"].astype(str).str.strip()
    df["customerid"] = df["customerid"].astype(str)
    df["country"] = df["country"].astype(str).str.strip()

    return df


def get_valid_sales(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["is_valid_sale"]].copy()


def round_float(value: Any, digits: int = 2) -> float:
    return round(float(value), digits)


def describe_dataset() -> dict[str, Any]:
    df = load_data()

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
        "categorical_columns": df.select_dtypes(exclude="number").columns.tolist(),
        "date_min": str(df["invoice_date"].min().date())
        if not df["invoice_date"].isna().all()
        else None,
        "date_max": str(df["invoice_date"].max().date())
        if not df["invoice_date"].isna().all()
        else None,
        "total_missing_values": int(df.isna().sum().sum()),
    }


def check_missing_values() -> list[dict[str, Any]]:
    df = load_data()

    missing = df.isna().sum()
    result = []

    for column, count in missing.items():
        if count > 0:
            result.append(
                {
                    "column": column,
                    "missing_values": int(count),
                    "missing_percentage": round((count / len(df)) * 100, 2),
                }
            )

    if not result:
        return [
            {
                "column": "all_columns",
                "missing_values": 0,
                "missing_percentage": 0.0,
            }
        ]

    return result


def top_products_by_revenue(limit: int = 10) -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)
    limit = normalize_limit(limit)

    result = (
        sales.groupby(["stockcode", "description"], as_index=False)
        .agg(
            product=("description", "first"),
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            transactions=("invoiceno", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .head(limit)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def sales_by_country(limit: int = 10) -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)
    limit = normalize_limit(limit)

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


def top_customers_by_revenue(limit: int = 10) -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)
    limit = normalize_limit(limit)

    known_customers = sales[sales["customerid"] != "Unknown"].copy()

    result = (
        known_customers.groupby("customerid", as_index=False)
        .agg(
            customerid=("customerid", "first"),
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            orders=("invoiceno", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .head(limit)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def average_order_value_by_country(limit: int = 10) -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)
    limit = normalize_limit(limit)

    order_revenue = (
        sales.groupby(["country", "invoiceno"], as_index=False)
        .agg(order_revenue=("revenue", "sum"))
    )

    result = (
        order_revenue.groupby("country", as_index=False)
        .agg(
            country=("country", "first"),
            average_order_value=("order_revenue", "mean"),
            total_revenue=("order_revenue", "sum"),
            orders=("invoiceno", "nunique"),
        )
        .sort_values("average_order_value", ascending=False)
        .head(limit)
    )

    result["average_order_value"] = result["average_order_value"].round(2)
    result["total_revenue"] = result["total_revenue"].round(2)

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


def monthly_orders_trend() -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)

    result = (
        sales.groupby("invoice_month", as_index=False)
        .agg(
            month=("invoice_month", "first"),
            orders=("invoiceno", "nunique"),
            quantity=("quantity", "sum"),
            revenue=("revenue", "sum"),
        )
        .drop(columns=["invoice_month"])
        .sort_values("month")
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def monthly_average_order_value() -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)

    order_revenue = (
        sales.groupby(["invoice_month", "invoiceno"], as_index=False)
        .agg(order_revenue=("revenue", "sum"))
    )

    result = (
        order_revenue.groupby("invoice_month", as_index=False)
        .agg(
            month=("invoice_month", "first"),
            average_order_value=("order_revenue", "mean"),
            total_revenue=("order_revenue", "sum"),
            orders=("invoiceno", "nunique"),
        )
        .drop(columns=["invoice_month"])
        .sort_values("month")
    )

    result["average_order_value"] = result["average_order_value"].round(2)
    result["total_revenue"] = result["total_revenue"].round(2)

    return result.to_dict(orient="records")


def revenue_by_country_and_month(
    country: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)
    limit = normalize_limit(limit, max_limit=500)

    if country:
        sales = sales[
            sales["country"].str.lower() == country.strip().lower()
        ].copy()

    result = (
        sales.groupby(["country", "invoice_month"], as_index=False)
        .agg(
            country=("country", "first"),
            month=("invoice_month", "first"),
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            orders=("invoiceno", "nunique"),
        )
        .drop(columns=["invoice_month"])
        .sort_values(["country", "month"])
        .head(limit)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def top_products_by_country(country: str, limit: int = 10) -> list[dict[str, Any]]:
    df = load_data()
    sales = get_valid_sales(df)
    limit = normalize_limit(limit)

    filtered_sales = sales[
        sales["country"].str.lower() == country.strip().lower()
    ].copy()

    result = (
        filtered_sales.groupby(["stockcode", "description"], as_index=False)
        .agg(
            country=("country", "first"),
            product=("description", "first"),
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            transactions=("invoiceno", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .head(limit)
    )

    result["revenue"] = result["revenue"].round(2)

    return result.to_dict(orient="records")


def returns_analysis() -> dict[str, Any]:
    df = load_data()

    total_rows = len(df)
    return_rows = int(df["is_return"].sum())
    returns = df[df["is_return"]].copy()

    total_return_quantity = (
        int(returns["quantity"].abs().sum()) if not returns.empty else 0
    )
    total_return_value = (
        round_float(returns["revenue"].abs().sum()) if not returns.empty else 0.0
    )

    return {
        "total_rows": int(total_rows),
        "return_rows": return_rows,
        "return_percentage": round((return_rows / total_rows) * 100, 2)
        if total_rows
        else 0.0,
        "total_return_quantity": total_return_quantity,
        "total_return_value": total_return_value,
    }


def return_rate_by_product(
    limit: int = 10,
    min_transactions: int = 10,
) -> list[dict[str, Any]]:
    df = load_data()
    limit = normalize_limit(limit)

    grouped = (
        df.groupby(["stockcode", "description"], as_index=False)
        .agg(
            product=("description", "first"),
            total_rows=("invoiceno", "count"),
            return_rows=("is_return", "sum"),
            returned_quantity=("quantity", lambda x: int(x[x < 0].abs().sum())),
            returned_value=("revenue", lambda x: round_float(x[x < 0].abs().sum())),
        )
    )

    grouped = grouped[grouped["total_rows"] >= min_transactions].copy()

    grouped["return_rate"] = (
        grouped["return_rows"] / grouped["total_rows"] * 100
    ).round(2)

    result = (
        grouped.sort_values(["return_rate", "return_rows"], ascending=False)
        .head(limit)
    )

    return result.to_dict(orient="records")


def return_rate_by_country(limit: int = 10) -> list[dict[str, Any]]:
    df = load_data()
    limit = normalize_limit(limit)

    grouped = (
        df.groupby("country", as_index=False)
        .agg(
            country=("country", "first"),
            total_rows=("invoiceno", "count"),
            return_rows=("is_return", "sum"),
            returned_quantity=("quantity", lambda x: int(x[x < 0].abs().sum())),
            returned_value=("revenue", lambda x: round_float(x[x < 0].abs().sum())),
        )
    )

    grouped["return_rate"] = (
        grouped["return_rows"] / grouped["total_rows"] * 100
    ).round(2)

    result = (
        grouped.sort_values(["return_rate", "return_rows"], ascending=False)
        .head(limit)
    )

    return result.to_dict(orient="records")


def retail_summary() -> dict[str, Any]:
    df = load_data()
    sales = get_valid_sales(df)

    order_revenue = sales.groupby("invoiceno")["revenue"].sum()

    return {
        "rows": int(df.shape[0]),
        "valid_sales_rows": int(len(sales)),
        "return_rows": int(df["is_return"].sum()),
        "unique_orders": int(sales["invoiceno"].nunique()),
        "unique_products": int(sales["stockcode"].nunique()),
        "unique_customers": int(
            sales[sales["customerid"] != "Unknown"]["customerid"].nunique()
        ),
        "countries": int(sales["country"].nunique()),
        "total_revenue": round_float(sales["revenue"].sum()),
        "average_order_value": round_float(order_revenue.mean())
        if not order_revenue.empty
        else 0.0,
    }


def apply_filters(
    df: pd.DataFrame,
    filters: dict[str, Any] | None,
) -> pd.DataFrame:
    if not filters:
        return df.copy()

    filtered = df.copy()

    for raw_column, value in filters.items():
        column = normalize_column_name(raw_column)

        if column not in df.columns:
            raise ValueError(f"Unknown filter column: {raw_column}")

        if isinstance(value, list):
            normalized_values = [str(item).strip().lower() for item in value]
            filtered = filtered[
                filtered[column].astype(str).str.strip().str.lower().isin(
                    normalized_values
                )
            ].copy()

        elif isinstance(value, str):
            filtered = filtered[
                filtered[column].astype(str).str.strip().str.lower()
                == value.strip().lower()
            ].copy()

        else:
            filtered = filtered[filtered[column] == value].copy()

    return filtered


def flexible_groupby_analysis(
    group_by: list[str] | str,
    metric: str = "revenue",
    aggregation: str = "sum",
    filters: dict[str, Any] | None = None,
    valid_sales_only: bool = True,
    sort_descending: bool = True,
    limit: int = 20,
) -> list[dict[str, Any]]:
    df = load_data()
    limit = normalize_limit(limit, max_limit=500)

    if valid_sales_only:
        df = get_valid_sales(df)

    df = apply_filters(df, filters)

    if isinstance(group_by, str):
        group_columns = [group_by]
    else:
        group_columns = group_by

    group_columns = [normalize_column_name(column) for column in group_columns]
    metric_column = normalize_column_name(metric)
    aggregation = aggregation.strip().lower()

    for column in group_columns:
        if column not in ALLOWED_GROUP_COLUMNS:
            raise ValueError(f"Grouping by '{column}' is not allowed.")

    if metric_column not in ALLOWED_METRIC_COLUMNS:
        raise ValueError(f"Metric '{metric_column}' is not allowed.")

    if aggregation not in ALLOWED_AGGREGATIONS:
        raise ValueError(f"Aggregation '{aggregation}' is not allowed.")

    if df.empty:
        return []

    output_metric_name = f"{aggregation}_{metric_column}"

    if not group_columns:
        if aggregation == "sum":
            value = df[metric_column].sum()
        elif aggregation == "mean":
            value = df[metric_column].mean()
        elif aggregation == "median":
            value = df[metric_column].median()
        elif aggregation == "min":
            value = df[metric_column].min()
        elif aggregation == "max":
            value = df[metric_column].max()
        elif aggregation == "count":
            value = df[metric_column].count()
        elif aggregation == "nunique":
            value = df[metric_column].nunique()
        else:
            raise ValueError(f"Unsupported aggregation: {aggregation}")

        if isinstance(value, float):
            value = round(value, 2)

        return [{output_metric_name: value}]

    grouped = df.groupby(group_columns, as_index=False)

    if aggregation == "sum":
        result = grouped.agg(**{output_metric_name: (metric_column, "sum")})
    elif aggregation == "mean":
        result = grouped.agg(**{output_metric_name: (metric_column, "mean")})
    elif aggregation == "median":
        result = grouped.agg(**{output_metric_name: (metric_column, "median")})
    elif aggregation == "min":
        result = grouped.agg(**{output_metric_name: (metric_column, "min")})
    elif aggregation == "max":
        result = grouped.agg(**{output_metric_name: (metric_column, "max")})
    elif aggregation == "count":
        result = grouped.agg(**{output_metric_name: (metric_column, "count")})
    elif aggregation == "nunique":
        result = grouped.agg(**{output_metric_name: (metric_column, "nunique")})
    else:
        raise ValueError(f"Unsupported aggregation: {aggregation}")

    if pd.api.types.is_numeric_dtype(result[output_metric_name]):
        result[output_metric_name] = result[output_metric_name].round(2)

    result = (
        result.sort_values(output_metric_name, ascending=not sort_descending)
        .head(limit)
    )

    return result.to_dict(orient="records")