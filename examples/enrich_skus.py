"""Add UPC, brand, model, rating and category to a CSV of Best Buy SKUs.

    python enrich_skus.py products.csv --column sku --out products_enriched.csv

Reads the SKUs (or product URLs) in --column, looks them up on Best Buy 50 at
a time and writes the original rows with upc, brand, model, rating,
reviews_count, categories and the current price added.
"""

import argparse
import csv
import re

from quanticdata_bestbuy_scraper import BestBuyScraper, write

ADDED = ["upc", "brand", "model", "rating", "reviews_count", "categories", "price_value", "availability"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv_in")
    parser.add_argument("--column", default="sku", help="column with the SKU or product URL")
    parser.add_argument("--out", default="products_enriched.csv")
    args = parser.parse_args()

    with open(args.csv_in, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    skus = [r[args.column].strip() for r in rows if r.get(args.column)]

    bestbuy = BestBuyScraper()
    found = {}
    for i in range(0, len(skus), 50):
        batch = skus[i:i + 50]
        for p in bestbuy.product(batch, max_results=len(batch)):
            found[p["product_id"]] = p

    def sku_of(value: str) -> str:
        # Accept a bare SKU or a product URL that carries it (?skuId=6579457 or /sku/6579457).
        m = re.search(r"(?:skuId=|/sku/)(\d+)", value)
        return m.group(1) if m else value.strip()

    out = []
    for r in rows:
        p = found.get(sku_of(r.get(args.column) or ""), {})
        out.append({**r, **{k: p.get(k) for k in ADDED}})
    write(out, args.out)
    print(f"{sum(1 for r in out if r['upc'])} of {len(out)} rows enriched, written to {args.out}")


if __name__ == "__main__":
    main()
