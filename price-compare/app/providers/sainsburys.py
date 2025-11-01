"""Sainsbury's provider."""
from __future__ import annotations

from typing import Iterable, List

from .base import BaseProvider, ProviderError, map_fixture_results
from .helpers import filter_by_query, load_fixture
from ..schemas import ProductResult


class SainsburysProvider(BaseProvider):
    name = "sainsburys"
    retailer = "Sainsbury's"
    supports_live = True

    async def fetch_live(self, query: str) -> Iterable[dict]:
        raise ProviderError("Live Sainsbury's integration unavailable; falling back to fixtures")

    async def load_fixture(self, query: str) -> Iterable[dict]:
        data = load_fixture("sainsburys")
        return filter_by_query(data, query)

    def parse_results(self, raw: Iterable[dict]) -> List[ProductResult]:
        return map_fixture_results(raw)

