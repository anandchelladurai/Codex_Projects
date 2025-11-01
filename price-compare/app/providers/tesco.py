"""Tesco provider implementation."""
from __future__ import annotations

from typing import Iterable, List

from .base import BaseProvider, ProviderError, map_fixture_results
from .helpers import filter_by_query, load_fixture
from ..schemas import ProductResult


class TescoProvider(BaseProvider):
    name = "tesco"
    retailer = "Tesco"
    supports_live = True

    async def fetch_live(self, query: str) -> Iterable[dict]:
        raise ProviderError("Live Tesco integration is not available in this demo build; using fixtures")

    async def load_fixture(self, query: str) -> Iterable[dict]:
        data = load_fixture("tesco")
        return filter_by_query(data, query)

    def parse_results(self, raw: Iterable[dict]) -> List[ProductResult]:
        return map_fixture_results(raw)

