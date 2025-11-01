"""Waitrose provider."""
from __future__ import annotations

from typing import Iterable, List

from .base import BaseProvider, map_fixture_results
from .helpers import filter_by_query, load_fixture
from ..schemas import ProductResult


class WaitroseProvider(BaseProvider):
    name = "waitrose"
    retailer = "Waitrose"

    async def fetch_live(self, query: str) -> Iterable[dict]:
        return []

    async def load_fixture(self, query: str) -> Iterable[dict]:
        data = load_fixture("waitrose")
        return filter_by_query(data, query)

    def parse_results(self, raw: Iterable[dict]) -> List[ProductResult]:
        return map_fixture_results(raw)

