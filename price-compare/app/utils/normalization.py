"""Functions for normalizing product sizes and deduplicating SKUs."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from . import parsing
from .units import NormalizedUnit, compute_unit_price, normalize_count, normalize_volume, normalize_weight

SIZE_REGEX = re.compile(
    r"(?P<multi>\d+(?:\.\d+)?)\s*[x×]\s*(?P<size>\d+(?:\.\d+)?)\s*(?P<unit>kg|g|l|ml|pack|pcs|count|item)s?",
    re.I,
)
SIMPLE_SIZE_REGEX = re.compile(r"(?P<size>\d+(?:\.\d+)?)\s*(?P<unit>kg|g|l|ml|pack|pcs|count|item)s?", re.I)


@dataclass
class NormalizedSize:
    """Structured representation of a size string."""

    display: str
    quantity: float
    unit: str
    normalized_unit: Optional[NormalizedUnit]


def parse_size(size_text: str) -> NormalizedSize:
    """Parse textual size descriptions into structured data."""

    text = size_text.strip()
    multi_match = SIZE_REGEX.search(text)
    if multi_match:
        multiplier = float(multi_match.group("multi"))
        size = float(multi_match.group("size"))
        unit = multi_match.group("unit").lower()
        quantity = multiplier * size
        guessed = False
    else:
        match = SIMPLE_SIZE_REGEX.search(text)
        if match:
            quantity = float(match.group("size"))
            unit = match.group("unit").lower()
            guessed = False
        else:
            quantity = 1.0
            unit = "count"
            guessed = True
    normalized = None if guessed else _normalize_quantity(quantity, unit)
    return NormalizedSize(display=text or "1 count", quantity=quantity, unit=unit, normalized_unit=normalized)


def _normalize_quantity(quantity: float, unit: str) -> Optional[NormalizedUnit]:
    """Normalize quantity/unit pair."""

    weight = normalize_weight(quantity, unit)
    if weight:
        return weight
    volume = normalize_volume(quantity, unit)
    if volume:
        return volume
    return normalize_count(quantity, unit)


def calculate_unit_price(total_price: float, size_text: str) -> Tuple[float, Optional[NormalizedUnit]]:
    """Return unit price from textual size."""

    normalized_size = parse_size(size_text)
    unit_price = compute_unit_price(total_price, normalized_size.normalized_unit)
    if unit_price is None:
        unit_price = round(total_price, 2)
    return unit_price, normalized_size.normalized_unit


def deduplicate_results(results: Iterable[str]) -> list[str]:
    """Return deduplicated results maintaining order, case-insensitive."""

    seen = set()
    output = []
    for title in results:
        key = " ".join(sorted(parsing.tokenize(title)))
        if key not in seen:
            seen.add(key)
            output.append(title)
    return output

