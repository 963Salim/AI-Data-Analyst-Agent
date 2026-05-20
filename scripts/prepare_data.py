import pandas as pd
from pathlib import Path

RAW_PATH = Path("D:/AI Data Analyst Agent/Dataset/archive/online_retail.csv")
PROCESSED_DIR = Path("data/processed")
PROCESSED_PATH = PROCESSED_DIR / "retail_clean.csv"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_PATH, encoding="ISO-8859-1", low_memory=False)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")

df = df.dropna(subset=["description"])

df["customerid"] = df["customerid"].fillna("Unknown").astype(str)

df["description"] = df["description"].astype(str).str.strip()
df["country"] = df["country"].astype(str).str.strip()

df["is_return"] = df["quantity"] < 0
df["revenue"] = df["quantity"] * df["unitprice"]
df["invoice_month"] = df["invoicedate"].dt.to_period("M").astype(str)
df["invoice_date"] = df["invoicedate"].dt.date.astype(str)

df["is_valid_sale"] = (
    (df["quantity"] > 0)
    & (df["unitprice"] > 0)
    & (~df["invoicedate"].isna())
)

df.to_csv(PROCESSED_PATH, index=False)

print("Processed data saved to:")
print(PROCESSED_PATH)

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isna().sum())

print("\nReturns:")
print(df["is_return"].value_counts())

print("\nValid sales:")
print(df["is_valid_sale"].value_counts())

print("\nRevenue summary:")
print(df["revenue"].describe())