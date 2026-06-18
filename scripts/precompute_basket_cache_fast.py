import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "processed" / "retail_clean.csv"
CACHE_DIR = BASE_DIR / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = CACHE_DIR / "spark_basket_product_pairs.json"


MAX_PRODUCTS_PER_INVOICE = 60
TOP_N_PAIRS = 100


def normalize_boolean(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .isin({"true", "1", "yes", "y"})
    )


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {INPUT_PATH}. "
            "Run scripts/prepare_data.py first."
        )

    print("Loading processed retail dataset...")
    df = pd.read_csv(INPUT_PATH, low_memory=False)

    required_columns = {
        "invoiceno",
        "stockcode",
        "description",
        "is_valid_sale",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "The processed dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    df["is_valid_sale"] = normalize_boolean(df["is_valid_sale"])

    sales = df[df["is_valid_sale"]].copy()

    sales["invoiceno"] = sales["invoiceno"].astype(str)
    sales["stockcode"] = sales["stockcode"].astype(str).str.strip().str.upper()
    sales["description"] = sales["description"].astype(str).str.strip()

    sales = sales[
        (sales["invoiceno"] != "")
        & (sales["stockcode"] != "")
        & (sales["description"] != "")
    ].copy()

    print("Creating invoice-product table...")

    items = (
        sales[["invoiceno", "stockcode", "description"]]
        .drop_duplicates(subset=["invoiceno", "stockcode"])
        .copy()
    )

    product_name_by_code = (
        items.groupby("stockcode")["description"]
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0])
        .to_dict()
    )

    print("Building product pairs...")

    pair_counter: Counter[tuple[str, str]] = Counter()

    grouped = items.groupby("invoiceno")["stockcode"].apply(list)

    skipped_large_invoices = 0

    for product_codes in grouped:
        unique_codes = sorted(set(product_codes))

        if len(unique_codes) < 2:
            continue

        if len(unique_codes) > MAX_PRODUCTS_PER_INVOICE:
            skipped_large_invoices += 1
            continue

        for product_a_code, product_b_code in combinations(unique_codes, 2):
            pair_counter[(product_a_code, product_b_code)] += 1

    print(f"Skipped large invoices: {skipped_large_invoices}")
    print("Preparing output...")

    records = []

    for (product_a_code, product_b_code), shared_orders in pair_counter.most_common(TOP_N_PAIRS):
        records.append(
            {
                "product_a_code": product_a_code,
                "product_a": product_name_by_code.get(product_a_code, "Unknown"),
                "product_b_code": product_b_code,
                "product_b": product_name_by_code.get(product_b_code, "Unknown"),
                "shared_orders": int(shared_orders),
            }
        )

    OUTPUT_PATH.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Saved: {OUTPUT_PATH}")
    print(f"Rows saved: {len(records)}")


if __name__ == "__main__":
    main()