"""
MySQL Database Schema + Data Loader
Creates the ecommerce_analysis DB, tables, and loads cleaned CSV data.
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ── CONFIG ─── Update these with your MySQL credentials ──────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",        # ← your MySQL username
    "password": "root@1234",  # ← your MySQL password
}
DB_NAME       = "ecommerce_analysis"
CLEANED_CSV   = "/cleaned_products.csv"


# ── SQL STATEMENTS ────────────────────────────────────────────────────────────
CREATE_DB = f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"

CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(500)   NOT NULL,
    brand           VARCHAR(100),
    category        VARCHAR(100),
    price_gbp       DECIMAL(10,2),
    mrp_gbp         DECIMAL(10,2),
    discount_pct    DECIMAL(5,2),
    rating          TINYINT,
    review_count    INT,
    availability    VARCHAR(50),
    price_tier      VARCHAR(30),
    discount_bucket VARCHAR(20),
    rating_label    VARCHAR(20),
    savings_gbp     DECIMAL(10,2),
    high_value_deal TINYINT(1),
    review_tier     VARCHAR(20),
    detail_url      TEXT,
    scraped_at      DATETIME,
    INDEX idx_brand    (brand),
    INDEX idx_category (category),
    INDEX idx_rating   (rating),
    INDEX idx_discount (discount_pct)
);
"""

INSERT_PRODUCT = """
INSERT INTO products
    (title, brand, category, price_gbp, mrp_gbp, discount_pct,
     rating, review_count, availability, price_tier, discount_bucket,
     rating_label, savings_gbp, high_value_deal, review_tier,
     detail_url, scraped_at)
VALUES
    (%(title)s, %(brand)s, %(category)s, %(price_gbp)s, %(mrp_gbp)s,
     %(discount_pct)s, %(rating)s, %(review_count)s, %(availability)s,
     %(price_tier)s, %(discount_bucket)s, %(rating_label)s, %(savings_gbp)s,
     %(high_value_deal)s, %(review_tier)s, %(detail_url)s, %(scraped_at)s)
"""

# ── Useful analytical views ───────────────────────────────────────────────────
CREATE_VIEWS = [
    """
    CREATE OR REPLACE VIEW vw_brand_summary AS
    SELECT
        brand,
        COUNT(*)                        AS total_products,
        ROUND(AVG(rating), 2)           AS avg_rating,
        ROUND(AVG(discount_pct), 2)     AS avg_discount,
        ROUND(AVG(price_gbp), 2)        AS avg_price,
        SUM(review_count)               AS total_reviews
    FROM products
    GROUP BY brand
    ORDER BY avg_rating DESC;
    """,
    """
    CREATE OR REPLACE VIEW vw_category_summary AS
    SELECT
        category,
        COUNT(*)                        AS total_products,
        ROUND(AVG(price_gbp), 2)        AS avg_price,
        MAX(price_gbp)                  AS max_price,
        MIN(price_gbp)                  AS min_price,
        ROUND(AVG(discount_pct), 2)     AS avg_discount,
        ROUND(AVG(rating), 2)           AS avg_rating
    FROM products
    GROUP BY category
    ORDER BY avg_price DESC;
    """,
    """
    CREATE OR REPLACE VIEW vw_top_discounted AS
    SELECT
        title, brand, category,
        price_gbp, mrp_gbp, discount_pct, savings_gbp, rating
    FROM products
    ORDER BY discount_pct DESC
    LIMIT 50;
    """,
    """
    CREATE OR REPLACE VIEW vw_high_value_deals AS
    SELECT
        title, brand, category,
        price_gbp, discount_pct, rating, review_count
    FROM products
    WHERE high_value_deal = 1
    ORDER BY rating DESC, discount_pct DESC;
    """,
]


# ── FUNCTIONS ─────────────────────────────────────────────────────────────────
def get_connection(database: str = None):
    cfg = {**DB_CONFIG}
    if database:
        cfg["database"] = database
    return mysql.connector.connect(**cfg)


def setup_database():
    """Create DB + tables + views."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(CREATE_DB)
    logger.info(f"Database '{DB_NAME}' ensured")

    cursor.execute(f"USE {DB_NAME}")
    cursor.execute(CREATE_PRODUCTS_TABLE)
    logger.info("Table 'products' ensured")

    for view_sql in CREATE_VIEWS:
        cursor.execute(view_sql)
    logger.info(f"Created {len(CREATE_VIEWS)} analytical views")

    conn.commit()
    cursor.close()
    conn.close()


def load_data(csv_path: str):
    """Load cleaned CSV into the products table (truncate first)."""
    df = pd.read_csv(csv_path)
    logger.info(f"Loading {len(df)} rows from {csv_path}")

    conn = get_connection(database=DB_NAME)
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE products")  # fresh load each run
    logger.info("Table truncated for fresh load")

    # Convert NaN → None (MySQL NULL)
    records = df.where(pd.notnull(df), None).to_dict("records")

    cursor.executemany(INSERT_PRODUCT, records)
    conn.commit()

    logger.info(f"✅ Inserted {cursor.rowcount} rows into 'products'")
    cursor.close()
    conn.close()


def run_sample_queries():
    """Print results of useful analytical queries."""
    conn = get_connection(database=DB_NAME)
    cursor = conn.cursor(dictionary=True)

    queries = {
        "Top 5 Brands by Avg Rating":
            "SELECT brand, avg_rating, total_products FROM vw_brand_summary LIMIT 5;",
        "Top 5 Categories by Avg Price":
            "SELECT category, avg_price, total_products FROM vw_category_summary LIMIT 5;",
        "Top 5 Discounted Products":
            "SELECT title, brand, discount_pct, savings_gbp FROM vw_top_discounted LIMIT 5;",
        "High Value Deals Count":
            "SELECT COUNT(*) AS deals FROM vw_high_value_deals;",
    }

    for title, sql in queries.items():
        print(f"\n── {title} ──────────────────────────────")
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)

    cursor.close()
    conn.close()


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        setup_database()
        load_data(CLEANED_CSV)
        run_sample_queries()
        print("\n✅ Database setup and data load complete!")
    except Error as e:
        logger.error(f"MySQL error: {e}")
