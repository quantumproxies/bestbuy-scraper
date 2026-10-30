"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class BestbuyProductRow(TypedDict, total=False):
    """One row of `bestbuy-scraper product` (bestbuy_product v1.1.0)."""

    retailer: str
    """Retailer the row comes from (bestbuy)."""
    product_id: str
    """Best Buy SKU."""
    url: str
    """Product URL."""
    title: Optional[str]
    """Product title."""
    brand: Optional[str]
    """Brand."""
    model: Optional[str]
    """Model number when the retailer exposes it."""
    upc: Optional[str]
    """UPC/GTIN as the retailer records it."""
    price: str
    """Current selling price as shown."""
    price_value: float
    """Numeric current price, from the retailer's own offer data."""
    currency: str
    """Currency (USD)."""
    regular_price_value: Optional[float]
    """Regular/was price; equals price_value when not discounted."""
    on_sale: bool
    """True when the current price is below the regular price."""
    availability: str
    """in_stock | out_of_stock | unknown."""
    availability_detail: Optional[str]
    """The retailer's own stock status."""
    seller: Optional[str]
    """Who sells this offer."""
    seller_type: Optional[str]
    """retailer (first party) | marketplace."""
    condition: Optional[str]
    """Condition (new, refurbished...)."""
    price_source: str
    """The Best Buy data field the price was read from."""
    checked_at: str
    """When the price was read (ISO 8601)."""
    rating: Optional[float]
    """Average star rating."""
    reviews_count: Optional[int]
    """Number of reviews."""
    image: Optional[str]
    """Main product image URL."""
    categories: List[str]
    """Category path."""
