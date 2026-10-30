"""Best Buy SKUs that are at or under the price you want to pay.

    python price_alert.py wishlist.csv --out alerts.csv

wishlist.csv has two columns, sku and target_price:

    sku,target_price
    6579457,299.99

The script reads the current Best Buy price of every SKU, prints the ones at or
under their target price and writes them to alerts.csv. Run it from cron and
the printed lines become your alert.
"""

import argparse
import csv

from quanticdata_bestbuy_scraper import BestBuyScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("wishlist", help="CSV with columns sku,target_price")
    parser.add_argument("--out", default="alerts.csv")
    args = parser.parse_args()

    with open(args.wishlist, newline="", encoding="utf-8") as fh:
        targets = {row["sku"].strip(): float(row["target_price"]) for row in csv.DictReader(fh) if row.get("sku")}

    bestbuy = BestBuyScraper()
    skus = list(targets)
    hits = []
    for i in range(0, len(skus), 50):
        batch = skus[i:i + 50]
        for p in bestbuy.product(batch, max_results=len(batch)):
            target = targets.get(p["product_id"])
            if target is not None and p.get("price_value") is not None and p["price_value"] <= target:
                hits.append({"sku": p["product_id"], "target_price": target, "price_value": p["price_value"],
                             "regular_price_value": p.get("regular_price_value"), "on_sale": p.get("on_sale"),
                             "availability": p.get("availability"), "title": p.get("title"), "url": p.get("url")})

    for h in hits:
        print(f"{h['sku']}: {h['price_value']} <= {h['target_price']}  {h['title']}")
    write(hits, args.out)
    print(f"{len(hits)} of {len(skus)} SKUs at or under their target, written to {args.out}")


if __name__ == "__main__":
    main()
