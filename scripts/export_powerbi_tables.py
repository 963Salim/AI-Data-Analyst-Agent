from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "processed" / "retail_clean.csv"
EXPORT_DIR = BASE_DIR / "exports" / "powerbi"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(value: Any, default: str = "Unknown") -> str:
    """Convert values to clean text for stable Power BI keys."""
    if pd.isna(value):
        return default

    text = str(value).strip()

    if text.lower() in {"", "nan", "none", "null"}:
        return default

    return text


def clean_customer_id(value: Any) -> str:
    """
    Converts customer IDs into clean text values.
    This avoids Power BI errors caused by mixed numeric IDs and 'Unknown'.
    """
    text = clean_text(value, default="Unknown")

    if text == "Unknown":
        return text

    # Converts values like 17850.0 to 17850
    if text.endswith(".0"):
        try:
            return str(int(float(text)))
        except ValueError:
            return text

    return text


def mode_or_first(series: pd.Series) -> str:
    """
    Returns the most frequent non-empty value.
    Useful when the same product code has multiple descriptions.
    """
    cleaned = series.dropna().astype(str).str.strip()
    cleaned = cleaned[~cleaned.str.lower().isin(["", "nan", "none", "null"])]

    if cleaned.empty:
        return "Unknown"

    mode_values = cleaned.mode()

    if not mode_values.empty:
        return str(mode_values.iloc[0])

    return str(cleaned.iloc[0])


def export_csv(df: pd.DataFrame, filename: str) -> None:
    """
    Consistent CSV export for Power BI.
    utf-8-sig helps Power BI and Excel recognize encoding correctly.
    """
    df.to_csv(
        EXPORT_DIR / filename,
        index=False,
        encoding="utf-8-sig",
        sep=",",
        decimal=".",
        lineterminator="\n",
    )


def validate_unique_key(df: pd.DataFrame, key: str, table_name: str) -> None:
    """
    Ensures that dimension keys are unique.
    Power BI needs unique keys on the 1-side of a many-to-one relationship.
    """
    duplicate_count = df[key].duplicated().sum()

    if duplicate_count > 0:
        examples = (
            df.loc[df[key].duplicated(keep=False), key]
            .drop_duplicates()
            .head(10)
            .tolist()
        )

        raise ValueError(
            f"{table_name} contains {duplicate_count} duplicate key rows "
            f"for key '{key}'. Examples: {examples}"
        )


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_PATH}. "
            "Run scripts/prepare_data.py first."
        )

    df = pd.read_csv(INPUT_PATH, low_memory=False)

    # -------------------------
    # Clean and standardize types
    # -------------------------
    df["invoiceno"] = df["invoiceno"].apply(lambda x: clean_text(x, default="UnknownInvoice"))
    df["stockcode"] = (
    df["stockcode"]
    .apply(lambda x: clean_text(x, default="UnknownStock"))
    .str.upper()
)
    df["description"] = df["description"].apply(lambda x: clean_text(x, default="Unknown Product"))
    df["country"] = df["country"].apply(lambda x: clean_text(x, default="Unknown Country"))

    df["customerid"] = df["customerid"].apply(clean_customer_id)

    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce").dt.date
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    df["invoice_month"] = df["invoice_date"].dt.to_period("M").astype(str)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["unitprice"] = pd.to_numeric(df["unitprice"], errors="coerce").fillna(0)
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0)

    df["is_return"] = df["is_return"].astype(str).str.lower().eq("true")
    df["is_valid_sale"] = df["is_valid_sale"].astype(str).str.lower().eq("true")

    # -------------------------
    # Stable text keys for Power BI relationships
    # -------------------------
    df["customer_key"] = df["customerid"].apply(
        lambda x: "UNKNOWN_CUSTOMER" if x == "Unknown" else f"CUST_{x}"
    )

    df["product_key"] = df["stockcode"].apply(lambda x: f"SKU_{x}")
    df["country_key"] = df["country"].apply(lambda x: f"COUNTRY_{x}")

    # -------------------------
    # Business columns
    # -------------------------
    df["returned_value"] = 0.0
    df.loc[df["is_return"], "returned_value"] = (
        df.loc[df["is_return"], "quantity"].abs()
        * df.loc[df["is_return"], "unitprice"]
    )

    df["gross_sales_value"] = 0.0
    df.loc[df["is_valid_sale"], "gross_sales_value"] = df.loc[
        df["is_valid_sale"], "revenue"
    ]

    df["net_sales_value"] = df["gross_sales_value"] - df["returned_value"]

    # -------------------------
    # Fact Table
    # -------------------------
    fact_sales = df[
        [
            "invoiceno",
            "product_key",
            "customer_key",
            "country_key",
            "stockcode",
            "customerid",
            "country",
            "invoice_date",
            "invoice_month",
            "quantity",
            "unitprice",
            "revenue",
            "gross_sales_value",
            "returned_value",
            "net_sales_value",
            "is_return",
            "is_valid_sale",
        ]
    ].copy()

    export_csv(fact_sales, "fact_sales.csv")

    # -------------------------
    # Dimension: Date
    # -------------------------
    dim_date = (
        df[["invoice_date"]]
        .dropna()
        .drop_duplicates()
        .sort_values("invoice_date")
        .copy()
    )

    dim_date["year"] = dim_date["invoice_date"].dt.year
    dim_date["month"] = dim_date["invoice_date"].dt.month
    dim_date["month_name"] = dim_date["invoice_date"].dt.month_name()
    dim_date["quarter"] = "Q" + dim_date["invoice_date"].dt.quarter.astype(str)
    dim_date["year_month"] = dim_date["invoice_date"].dt.to_period("M").astype(str)

    validate_unique_key(dim_date, "invoice_date", "dim_date")
    export_csv(dim_date, "dim_date.csv")

    # -------------------------
    # Dimension: Product
    # -------------------------
    # Important:
    # Same stockcode can appear with multiple descriptions.
    # Therefore we group by product_key and choose one representative description.
    dim_product = (
        df[["product_key", "stockcode", "description"]]
        .dropna(subset=["product_key"])
        .copy()
    )

    dim_product = (
        dim_product
        .groupby("product_key", as_index=False)
        .agg(
            stockcode=("stockcode", mode_or_first),
            description=("description", mode_or_first),
        )
        .sort_values("product_key")
    )

    validate_unique_key(dim_product, "product_key", "dim_product")
    export_csv(dim_product, "dim_product.csv")

    # -------------------------
    # Dimension: Customer
    # -------------------------
    dim_customer = (
        df[["customer_key", "customerid"]]
        .dropna(subset=["customer_key"])
        .copy()
    )

    dim_customer = (
        dim_customer
        .groupby("customer_key", as_index=False)
        .agg(customerid=("customerid", mode_or_first))
        .sort_values("customer_key")
    )

    dim_customer["is_unknown_customer"] = dim_customer["customer_key"].eq("UNKNOWN_CUSTOMER")

    validate_unique_key(dim_customer, "customer_key", "dim_customer")
    export_csv(dim_customer, "dim_customer.csv")

    # -------------------------
    # Dimension: Country
    # -------------------------
    dim_country = (
        df[["country_key", "country"]]
        .dropna(subset=["country_key"])
        .copy()
    )

    dim_country = (
        dim_country
        .groupby("country_key", as_index=False)
        .agg(country=("country", mode_or_first))
        .sort_values("country_key")
    )

    validate_unique_key(dim_country, "country_key", "dim_country")
    export_csv(dim_country, "dim_country.csv")

    # -------------------------
    # KPI Summary
    # -------------------------
    valid_sales = df[df["is_valid_sale"]].copy()
    returns = df[df["is_return"]].copy()

    total_revenue = valid_sales["revenue"].sum()
    total_orders = valid_sales["invoiceno"].nunique()
    returned_value = returns["returned_value"].sum()

    kpi_summary = pd.DataFrame(
        [
            {
                "total_rows": int(len(df)),
                "valid_sales_rows": int(len(valid_sales)),
                "invalid_sales_rows": int(len(df) - len(valid_sales)),
                "total_revenue": round(float(total_revenue), 2),
                "total_orders": int(total_orders),
                "average_order_value": round(float(total_revenue / total_orders), 2)
                if total_orders
                else 0,
                "return_rows": int(len(returns)),
                "returned_value": round(float(returned_value), 2),
                "return_value_rate": round(float(returned_value / total_revenue), 4)
                if total_revenue
                else 0,
                "countries": int(valid_sales["country_key"].nunique()),
                "products": int(valid_sales["product_key"].nunique()),
                "customers": int(
                    valid_sales.loc[
                        valid_sales["customer_key"] != "UNKNOWN_CUSTOMER",
                        "customer_key",
                    ].nunique()
                ),
                "unknown_customer_rows": int(
                    (df["customer_key"] == "UNKNOWN_CUSTOMER").sum()
                ),
            }
        ]
    )

    export_csv(kpi_summary, "kpi_summary.csv")

    # -------------------------
    # Data Quality Summary
    # -------------------------
    missing = df.isna().sum().reset_index()
    missing.columns = ["column_name", "missing_values"]
    missing["missing_percentage"] = (
        missing["missing_values"] / len(df) * 100
    ).round(2)

    export_csv(missing, "data_quality_summary.csv")

    # -------------------------
    # Duplicate check report
    # -------------------------
    print("Power BI export completed.")
    print(f"Files saved to: {EXPORT_DIR}")
    print()
    print("Dimension key checks:")
    print(f"- dim_date:     {dim_date['invoice_date'].duplicated().sum()} duplicate keys")
    print(f"- dim_product:  {dim_product['product_key'].duplicated().sum()} duplicate keys")
    print(f"- dim_customer: {dim_customer['customer_key'].duplicated().sum()} duplicate keys")
    print(f"- dim_country:  {dim_country['country_key'].duplicated().sum()} duplicate keys")
    print()
    print("Rows exported:")
    print(f"- fact_sales:            {len(fact_sales):,}")
    print(f"- dim_date:              {len(dim_date):,}")
    print(f"- dim_product:           {len(dim_product):,}")
    print(f"- dim_customer:          {len(dim_customer):,}")
    print(f"- dim_country:           {len(dim_country):,}")
    print(f"- kpi_summary:           {len(kpi_summary):,}")
    print(f"- data_quality_summary:  {len(missing):,}")


if __name__ == "__main__":
    main()