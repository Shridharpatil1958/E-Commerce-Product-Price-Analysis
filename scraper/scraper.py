"""
E-Commerce Product Price Scraper
Scrapes product data: name, brand, price, discount, rating, reviews
Target: books.toscrape.com (free, legal practice site)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
import os
from datetime import datetime

# ── LOGGING SETUP ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ── CONFIG ────────────────────────────────────────────────────
BASE_URL = "https://books.toscrape.com/catalogue/"
MAX_PAGES = 10

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

DELAY_RANGE = (1, 3)

# ── HELPER DATA ───────────────────────────────────────────────
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

BRANDS = [
    "PenguinBooks",
    "HarperCollins",
    "RandomHouse",
    "Macmillan",
    "SimonSchuster",
    "HachetteBook",
    "OxfordPress",
    "CambridgePress",
    "Bloomsbury",
    "Scholastic"
]

CATEGORIES = [
    "Fiction",
    "Non-Fiction",
    "Science",
    "History",
    "Biography",
    "Technology",
    "Self-Help",
    "Children"
]

# ── FUNCTIONS ─────────────────────────────────────────────────


def get_page(url):
    """Fetch HTML page"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as e:
        logger.error(f"Failed to fetch {url} : {e}")
        return None


def parse_price(price_str):
    """Convert price string to float"""
    return float(price_str.replace("£", "").replace("Â", "").strip())


def simulate_mrp(price):
    """Generate fake original price"""
    margin = random.uniform(0.05, 0.50)
    return round(price * (1 + margin), 2)


def compute_discount(mrp, price):
    """Calculate discount percent"""
    return round(((mrp - price) / mrp) * 100, 2)


def scrape_product_list(page_num):
    """Scrape products from a page"""

    url = f"{BASE_URL}page-{page_num}.html"

    soup = get_page(url)

    if soup is None:
        return []

    products = []

    articles = soup.find_all("article", class_="product_pod")

    for article in articles:

        try:

            title = article.h3.a["title"]

            price_tag = article.find("p", class_="price_color")
            price = parse_price(price_tag.text)

            rating_class = article.find(
                "p", class_="star-rating")["class"][1]

            rating = RATING_MAP.get(rating_class, 0)

            availability = article.find(
                "p", class_="instock").text.strip()

            detail_url = BASE_URL + article.h3.a["href"].replace("../", "")

            # simulated fields
            mrp = simulate_mrp(price)
            discount_pct = compute_discount(mrp, price)
            brand = random.choice(BRANDS)
            category = random.choice(CATEGORIES)
            review_count = random.randint(5, 2000)

            scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            products.append({
                "title": title,
                "brand": brand,
                "category": category,
                "price_gbp": price,
                "mrp_gbp": mrp,
                "discount_pct": discount_pct,
                "rating": rating,
                "review_count": review_count,
                "availability": availability,
                "detail_url": detail_url,
                "scraped_at": scraped_at
            })

        except Exception as e:
            logger.warning(f"Product parse error: {e}")

    logger.info(f"Page {page_num}: scraped {len(products)} products")

    return products


def run_scraper():

    all_products = []

    for page in range(1, MAX_PAGES + 1):

        logger.info(f"Scraping page {page}/{MAX_PAGES}")

        products = scrape_product_list(page)

        all_products.extend(products)

        time.sleep(random.uniform(*DELAY_RANGE))

    df = pd.DataFrame(all_products)

    logger.info(f"Total products scraped: {len(df)}")

    return df


# ── MAIN PROGRAM ──────────────────────────────────────────────

if __name__ == "__main__":

    df = run_scraper()

    # create data directory automatically
    os.makedirs("data", exist_ok=True)

    output_path = "data/raw_products.csv"

    df.to_csv(output_path, index=False)

    logger.info(f"Data saved to {output_path}")

    print("\nSample Data:")
    print(df.head())