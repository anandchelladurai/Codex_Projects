"""Dataclasses representing requests and responses."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class SearchRequest:
    query: str
    live: bool = False
    indian_only: bool = False
    sort_by: str = "unit"

    def __post_init__(self) -> None:
        self.query = self.query.strip()
        if len(self.query) < 2 or len(self.query) > 120:
            raise ValueError("Query must be between 2 and 120 characters")
        if self.sort_by not in {"unit", "total"}:
            raise ValueError("sort_by must be 'unit' or 'total'")


@dataclass
class ProductResult:
    retailer: str
    title: str
    url: str
    size: str
    total_price: float
    unit_price: float
    last_checked: datetime
    image_url: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    currency: str = "GBP"
    in_stock: bool = True


@dataclass
class SearchResponse:
    results: List[ProductResult]
    warnings: List[str] = field(default_factory=list)

