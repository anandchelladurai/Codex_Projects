"""Base provider definition."""
from __future__ import annotations

import asyncio
import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Iterable, List, Optional

from ..config import get_settings
from ..schemas import ProductResult
from ..utils import normalization, parsing
from ..utils.rate_limit import RateLimiter

USER_AGENT = "UKPriceCompareBot/1.0 (+https://example.com)"


class ProviderError(Exception):
    """Raised for provider errors."""


class BaseProvider(ABC):
    """Abstract provider implementing common behaviours."""

    name: str
    retailer: str
    supports_live: bool = False

    def __init__(self) -> None:
        settings = get_settings()
        self.rate_limiter = RateLimiter(settings.rate_limit_qps)
        self.timeout = settings.provider_timeouts.get(self.name, settings.request_timeout)
        self._warning_callback: Optional[Callable[[str], None]] = None

    async def search(self, query: str, live: bool = False, indian_only: bool = False) -> List[ProductResult]:
        """Search provider for products matching query."""

        raw_results = []
        if live and self.supports_live:
            try:
                if not self.rate_limiter.acquire():
                    raise ProviderError("rate limited")
                raw_results = await self.fetch_live(query)
            except Exception as exc:  # noqa: BLE001
                raw_results = []
                await asyncio.sleep(random.uniform(0.1, 0.3))
                self.on_warning(f"{self.retailer}: live fetch failed ({exc})")
        if not raw_results:
            raw_results = await self.load_fixture(query)
        products = self.parse_results(raw_results)
        results = []
        query_tokens = parsing.tokenize(query)
        dedup_titles = normalization.deduplicate_results(item.title for item in products)
        for product in products:
            if product.title not in dedup_titles:
                continue
            if indian_only and not parsing.has_indian_brand(product.title):
                continue
            results.append(product)
        return results

    def on_warning(self, message: str) -> None:
        """Hook for warnings."""

        if self._warning_callback:
            self._warning_callback(message)

    @abstractmethod
    async def fetch_live(self, query: str) -> Iterable[dict]:
        """Fetch raw live data."""

    @abstractmethod
    async def load_fixture(self, query: str) -> Iterable[dict]:
        """Load mock data for offline mode."""

    @abstractmethod
    def parse_results(self, raw: Iterable[dict]) -> List[ProductResult]:
        """Convert raw payload to products."""

    def set_warning_callback(self, callback: Callable[[str], None] | None) -> None:
        """Register a callback for warning messages."""

        self._warning_callback = callback


def map_fixture_results(fixture: Iterable[dict]) -> List[ProductResult]:
    """Helper to map fixture dictionaries to ProductResult instances."""

    products: List[ProductResult] = []
    for item in fixture:
        unit_price, normalized = normalization.calculate_unit_price(item["price"], item.get("size", "1 count"))
        products.append(
            ProductResult(
                retailer=item["retailer"],
                title=item["title"],
                url=item["url"],
                image_url=item.get("image_url"),
                size=item.get("size", "1 count"),
                quantity=normalized.quantity if normalized else None,
                unit=normalized.unit if normalized else None,
                total_price=round(item["price"], 2),
                unit_price=unit_price,
                currency="GBP",
                in_stock=item.get("in_stock", True),
                last_checked=datetime.utcnow(),
            )
        )
    return products

