# Best Buy Web Scraper

[![ci](https://github.com/quantumproxies/bestbuy-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/bestbuy-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Best Buy product data from Python or the command line: Best Buy's own current price for a list of SKUs, with the regular price, sale flag, stock status, seller, UPC, model, rating and category path, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/bestbuy-scraper
bestbuy-scraper login
bestbuy-scraper product 6579457 -o bestbuy_prices.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=bestbuy-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `bestbuy-scraper product` | SKUs or product URLs | Regular price, stock, seller, UPC, 23 fields per row | up to 50 |

The input is the Best Buy SKU, the number in the product URL (6579457 in bestbuy.com/site/6579457.p?skuId=6579457); the full URL works too. Every row is Best Buy's own offer for that SKU, in USD, read at the time shown in `checked_at`. A run delivers 10 products unless you raise `--max-results` (up to 50).

## Sample output

A real row from `bestbuy-scraper product 6579457 --max-results 1` (2026-10-23):

```json
{
  "upc": "846042088510",
  "url": "https://www.bestbuy.com/site/6579457.p?skuId=6579457",
  "brand": "TCL",
  "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/1b524759-8f06-4397-b44d-7dd6feb22f3e.jpg",
  "model": "55Q651G",
  "price": "$319.99",
  "title": "TCL - 55\" Class Q6-Series 4K UHD QLED Smart Google TV (2024)",
  "rating": 4.7,
  "seller": "Best Buy",
  "on_sale": false,
  "currency": "USD",
  "retailer": "bestbuy",
  "condition": "new",
  "categories": [
    "TV & Home Theater",
    "TVs",
    "All Flat-Screen TVs"
  ],
  "checked_at": "2026-10-23T09:50:45.102Z",
  "product_id": "6579457",
  "price_value": 319.99,
  "seller_type": "retailer",
  "availability": "in_stock",
  "price_source": "bestbuy:productBySkuId.price.customerPrice",
  "reviews_count": 986,
  "availability_detail": "ADD_TO_CART",
  "regular_price_value": 319.99
}
```

## Python

```python
from quanticdata_bestbuy_scraper import BestBuyScraper

bestbuy = BestBuyScraper()  # saved login, or QUANTICDATA_API_KEY

run = bestbuy.product(["6579457"])
tv = run.rows[0]
print(tv["title"], tv["price_value"], tv["regular_price_value"], tv["on_sale"], tv["availability"])
print(tv["upc"], tv["model"], tv["categories"])
run.to_csv("bestbuy_prices.csv")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Price history**: Check a list of SKUs every few hours and append price, regular price, sale flag and stock to a CSV. See [`examples/price_watch.py`](examples/price_watch.py).
- **Price alerts**: Keep a CSV of SKUs with the price you want to pay and list the ones at or under it right now. See [`examples/price_alert.py`](examples/price_alert.py).
- **SKU enrichment**: Add UPC, brand, model, rating and category path to a CSV of Best Buy SKUs, for catalog matching. See [`examples/enrich_skus.py`](examples/enrich_skus.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `bestbuy-scraper run <id> -o out.csv` collects it later.

### `bestbuy-scraper product`

Best Buy's own current price for a list of SKUs — regular price, stock, seller, UPC.

```
bestbuy-scraper product PRODUCTS [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `PRODUCTS` | string[] |  | Best Buy product URLs or SKUs (one per line). |
| `--max-results` | integer | `10` | How many products to deliver at most (1–50). You pay only for delivered products. |

## Output fields

<details><summary><code>bestbuy-scraper product</code>: 23 fields</summary>

| Field | Type | Description |
|---|---|---|
| `retailer` | string | Retailer the row comes from (bestbuy). |
| `product_id` | string | Best Buy SKU. |
| `url` | string | Product URL. |
| `title` | string or null | Product title. |
| `brand` | string or null | Brand. |
| `model` | string or null | Model number when the retailer exposes it. |
| `upc` | string or null | UPC/GTIN as the retailer records it. |
| `price` | string | Current selling price as shown. |
| `price_value` | number | Numeric current price, from the retailer's own offer data. |
| `currency` | string | Currency (USD). |
| `regular_price_value` | number or null | Regular/was price; equals price_value when not discounted. |
| `on_sale` | boolean | True when the current price is below the regular price. |
| `availability` | string | in_stock \| out_of_stock \| unknown. |
| `availability_detail` | string or null | The retailer's own stock status. |
| `seller` | string or null | Who sells this offer. |
| `seller_type` | string or null | retailer (first party) \| marketplace. |
| `condition` | string or null | Condition (new, refurbished...). |
| `price_source` | string | The Best Buy data field the price was read from. |
| `checked_at` | string | When the price was read (ISO 8601). |
| `rating` | number or null | Average star rating. |
| `reviews_count` | integer or null | Number of reviews. |
| `image` | string or null | Main product image URL. |
| `categories` | string[] | Category path. |

</details>

## Sign-in and API keys

- `bestbuy-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `bestbuy-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `bestbuy-scraper login --api-key`.
- `bestbuy-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered product, at the per-row price listed in the API reference; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=bestbuy-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/bestbuy_product/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"products": ["6579457"], "max_results": 1}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=bestbuy-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=bestbuy-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Best Buy scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price listed in the API reference. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send SKUs and get rows back; the requests run on QuanticData's side.

**Where do I find the SKU?**

In the product page URL: 6579457 in bestbuy.com/site/6579457.p?skuId=6579457. You can also pass the full product URL.

**How many products can one run return?**

Up to 50 products per run. The default is 10, so pass --max-results when you send more SKUs; you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). The category path is joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/price_watch.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Walmart Scraper API](https://github.com/quantumproxies/walmart-scraper): Walmart scraper API for Python and the command line.
- [Target Scraper API](https://github.com/quantumproxies/target-scraper-api): Target scraper API for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=bestbuy-scraper).
