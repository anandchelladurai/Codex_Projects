"""Ensure providers conform to expected interface."""
import asyncio
from typing import Iterable

from app.providers import get_providers
from app.schemas import ProductResult


def test_all_providers_return_products() -> None:
    providers = get_providers()
    for provider in providers.values():
        results = asyncio.run(provider.search("basmati rice", live=False))
        assert isinstance(results, Iterable)
        assert all(isinstance(item, ProductResult) for item in results)
        for item in results:
            assert item.retailer
            assert item.title
            assert item.url
            assert item.total_price > 0
            assert item.unit_price > 0

