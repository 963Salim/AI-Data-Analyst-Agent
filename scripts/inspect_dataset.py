import pandas as pd
from pathlib import Path

DATA_PATH = Path("D:/AI Data Analyst Agent/Dataset/archive/online_retail.csv")

print("CSV path:")
print(DATA_PATH)

print("\nResolved path:")
print(DATA_PATH.resolve())

print("\nFile exists?")
print(DATA_PATH.exists())

if not DATA_PATH.exists():
    raise FileNotFoundError(f"CSV file not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH, encoding="ISO-8859-1", low_memory=False)

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())