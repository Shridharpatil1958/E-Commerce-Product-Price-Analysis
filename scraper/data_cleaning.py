"""
Data Cleaning & Transformation Pipeline
Reads raw_products.csv → cleans → outputs cleaned_products.csv
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

RAW_PATH     = "C:/Users/Yash/Ecommerce_analysis/data/raw_products.csv"
CLEANED_PATH = "C:/Users/Yash/Ecommerce_analysis/data/cleaned_products.csv"


# ── 1. LOAD ──────────────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


# ── 2. INSPECT ───────────────────────────────────────────────────────────────
def inspect(df: pd.DataFrame):
    print("\n── Shape ──────────────────────────────")
    print(df.shape)
    print("\n── Data Types ─────────────────────────")
    print(df.dtypes)
    print("\n── Null Counts ────────────────────────")
    print(df.isnull().sum())
    print("\n── Duplicates ─────────────────────────")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print("\n── Sample ─────────────────────────────")
    print(df.head(3).to_string())


# ── 3. CLEAN ─────────────────────────────────────────────────────────────────
def clean(df: pd.DataFrame) -> pd.DataFrame:

    # 3a. Drop exact duplicates
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Dropped {before - len(df)} duplicate rows")

    # 3b. Strip whitespace from string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    # 3c. Ensure numeric types
    for col in ["price_gbp", "mrp_gbp", "discount_pct", "rating", "review_count"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3d. Fill missing numerics with column median
    for col in ["price_gbp", "mrp_gbp", "discount_pct", "rating", "review_count"]:
        median_val = df[col].median()
        missing    = df[col].isnull().sum()
        if missing:
            df[col].fillna(median_val, inplace=True)
            logger.info(f"Filled {missing} nulls in '{col}' with median={median_val:.2f}")

    # 3e. Fill missing strings with 'Unknown'
    for col in ["brand", "category", "availability"]:
        df[col].fillna("Unknown", inplace=True)

    # 3f. Remove rows where price ≤ 0
    before = len(df)
    df = df[df["price_gbp"] > 0]
    logger.info(f"Removed {before - len(df)} rows with price ≤ 0")

    # 3g. Cap discount at 0–95 %
    df["discount_pct"] = df["discount_pct"].clip(0, 95)

    # 3h. Rating must be 1–5
    df["rating"] = df["rating"].clip(1, 5)

    # 3i. Parse scraped_at as datetime
    df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")

    # 3j. Standardise text columns
    df["brand"]    = df["brand"].str.title()
    df["category"] = df["category"].str.title()
    df["title"]    = df["title"].str.strip()

    return df


# ── 4. FEATURE ENGINEERING ────────────────────────────────────────────────────
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:

    # Price tier
    df["price_tier"] = pd.cut(
        df["price_gbp"],
        bins=[0, 10, 20, 35, 60, float("inf")],
        labels=["Budget (<£10)", "Economy (£10–£20)",
                "Mid (£20–£35)", "Premium (£35–£60)", "Luxury (£60+)"]
    )

    # Discount bucket
    df["discount_bucket"] = pd.cut(
        df["discount_pct"],
        bins=[-1, 10, 25, 40, 60, 100],
        labels=["<10%", "10–25%", "25–40%", "40–60%", "60%+"]
    )

    # Rating label
    df["rating_label"] = df["rating"].map({
        1: "Very Poor", 2: "Poor", 3: "Average", 4: "Good", 5: "Excellent"
    })

    # Savings in GBP
    df["savings_gbp"] = (df["mrp_gbp"] - df["price_gbp"]).round(2)

    # High-value flag: top 25% discount AND rating >= 4
    q75 = df["discount_pct"].quantile(0.75)
    df["high_value_deal"] = ((df["discount_pct"] >= q75) & (df["rating"] >= 4)).astype(int)

    # Review volume tier
    df["review_tier"] = pd.cut(
        df["review_count"],
        bins=[0, 50, 200, 500, float("inf")],
        labels=["Low", "Moderate", "High", "Viral"]
    )

    logger.info("Feature engineering complete")
    return df


# ── 5. SAVE ───────────────────────────────────────────────────────────────────
def save(df: pd.DataFrame, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Cleaned data saved → {path}  ({len(df)} rows)")


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data(RAW_PATH)
    inspect(df)
    df = clean(df)
    df = engineer_features(df)
    save(df, CLEANED_PATH)

    print("\n── Final Column Summary ────────────────")
    print(df.dtypes)
    print(f"\n✅ Pipeline complete. Rows: {len(df)}, Columns: {len(df.columns)}")