"""Best Buy Web Scraper: Best Buy web scraper for Python and the command line: Best Buy's own current price for a list of SKUs or product URLs, with regular price, sale flag, stock status, seller, UPC, model and category, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_bestbuy_scraper import BestBuyScraper

    scraper = BestBuyScraper()   # saved login (`bestbuy-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.product(...)   # Best Buy's current price, stock and seller for SKUs
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["BestBuyScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class BestBuyScraper:
    """Best Buy Web Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="bestbuy-scraper/0.1.0 (+https://github.com/quantumproxies/bestbuy-scraper)", timeout=timeout)

    def product(
        self, products: Union[str, Sequence[str]],
        *,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Best Buy's own current price for a list of SKUs — regular price, stock, seller, UPC.

        Args:
            products: Best Buy product URLs or SKUs (one per line).
            max_results: How many products to deliver at most (1–50). You pay only for delivered products.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per product: see ``types.BestbuyProductRow``.
        """
        payload = {
            "products": _as_list(products),
            "max_results": max_results,
        }
        return self.client.run_collector("bestbuy_product", payload, wait=wait, timeout=timeout)
