"""Track Best Buy prices over time.

Reads SKUs or product URLs from skus.txt (one per line), fetches Best Buy's
current price, regular price, sale flag and stock, and appends one row per
product to bestbuy_prices.csv with the time the price was read. Run it from cron:

    0 */6 * * *  cd /path/to/here && python price_watch.py --skus skus.txt

Needs a login (`bestbuy-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os

from quanticdata_bestbuy_scraper import BestBuyScraper

FIELDS = ["checked_at", "product_id", "title", "price_value", "regular_price_value", "on_sale",
          "availability", "availability_detail", "seller", "condition"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--skus", default="skus.txt", help="file with one SKU or product URL per line")
    parser.add_argument("--out", default="bestbuy_prices.csv")
    args = parser.parse_args()

    with open(args.skus, encoding="utf-8") as fh:
        skus = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    bestbuy = BestBuyScraper()
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        # One run takes up to 50 SKUs; max_results defaults to 10, so it is set to the batch size.
        for i in range(0, len(skus), 50):
            batch = skus[i:i + 50]
            for product in bestbuy.product(batch, max_results=len(batch)):
                writer.writerow(product)
                written += 1
    print(f"{written} prices appended to {args.out}")


if __name__ == "__main__":
    main()
