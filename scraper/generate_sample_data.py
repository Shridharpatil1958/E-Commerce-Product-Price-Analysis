"""
Sample Data Generator
Generates realistic e-commerce product data without requiring
internet access or MySQL — perfect for testing the full pipeline.
Run: python generate_sample_data.py
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
np.random.seed(42)

N_PRODUCTS = 500

BRANDS = [
    "PenguinBooks", "HarperCollins", "RandomHouse",
    "Macmillan", "SimonSchuster", "HachetteBook",
    "OxfordPress", "CambridgePress", "Bloomsbury", "Scholastic"
]

CATEGORIES = [
    "Fiction", "Non-Fiction", "Science", "History",
    "Biography", "Technology", "Self-Help", "Children"
]

ADJECTIVES = ["Amazing", "Essential", "Complete", "Ultimate", "Modern",
              "Advanced", "Practical", "Definitive", "Classic", "New"]
NOUNS      = ["Guide", "Handbook", "Collection", "Series", "Edition",
              "Companion", "Reference", "Anthology", "Masterclass", "Journal"]
TOPICS     = ["Python", "Data Science", "Leadership", "History", "Design",
              "Marketing", "Psychology", "Economics", "Health", "AI",
              "Travel", "Cooking", "Finance", "Philosophy", "Arts"]


def generate_title():
    return f"The {random.choice(ADJECTIVES)} {random.choice(TOPICS)} {random.choice(NOUNS)}"


def generate_price():
    tier = random.choices(
        ["budget", "economy", "mid", "premium", "luxury"],
        weights=[25, 35, 25, 10, 5]
    )[0]
    ranges = {
        "budget":  (2.99,  9.99),
        "economy": (10.00, 19.99),
        "mid":     (20.00, 34.99),
        "premium": (35.00, 59.99),
        "luxury":  (60.00, 120.00),
    }
    lo, hi = ranges[tier]
    return round(random.uniform(lo, hi), 2)


def generate_record():
    price        = generate_price()
    margin       = random.uniform(0.05, 0.55)
    mrp          = round(price * (1 + margin), 2)
    discount_pct = round(((mrp - price) / mrp) * 100, 2)
    rating       = random.choices([1, 2, 3, 4, 5], weights=[3, 7, 20, 45, 25])[0]
    review_count = int(np.random.lognormal(mean=4.5, sigma=1.5))
    review_count = max(1, min(review_count, 15000))

    base_time    = datetime(2025, 1, 1)
    delta_days   = random.randint(0, 180)
    scraped_at   = base_time + timedelta(days=delta_days,
                                          hours=random.randint(0, 23),
                                          minutes=random.randint(0, 59))
    return {
        "title":        generate_title(),
        "brand":        random.choice(BRANDS),
        "category":     random.choice(CATEGORIES),
        "price_gbp":    price,
        "mrp_gbp":      mrp,
        "discount_pct": discount_pct,
        "rating":       rating,
        "review_count": review_count,
        "availability": random.choices(
            ["In stock", "Out of stock"], weights=[85, 15])[0],
        "detail_url":   f"https://example.com/product/{random.randint(1000,9999)}",
        "scraped_at":   scraped_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


def main():
    records = [generate_record() for _ in range(N_PRODUCTS)]
    df      = pd.DataFrame(records)

    out = Path("../data/raw_products.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    print(f"✅ Generated {N_PRODUCTS} sample products → {out}")
    print(df.describe(include="all").to_string())


if __name__ == "__main__":
    main()