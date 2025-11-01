"""Utilities for unit conversion and normalization."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class NormalizedUnit:
    """Represents a normalized unit quantity."""

    quantity: float
    unit: str


BASE_CONVERSIONS = {
    "g": 1.0,
    "kg": 1000.0,
    "ml": 1.0,
    "l": 1000.0,
}


COUNT_UNITS = {"count", "pcs", "item"}


def normalize_weight(quantity: float, unit: str) -> Optional[NormalizedUnit]:
    """Normalize weight to grams."""

    unit = unit.lower()
    if unit not in {"g", "kg"}:
        return None
    grams = quantity * BASE_CONVERSIONS[unit]
    return NormalizedUnit(quantity=grams, unit="g")


def normalize_volume(quantity: float, unit: str) -> Optional[NormalizedUnit]:
    """Normalize volume to millilitres."""

    unit = unit.lower()
    if unit not in {"ml", "l"}:
        return None
    ml = quantity * BASE_CONVERSIONS[unit]
    return NormalizedUnit(quantity=ml, unit="ml")


def normalize_count(quantity: float, unit: str) -> Optional[NormalizedUnit]:
    """Normalize count-based units."""

    unit = unit.lower()
    if unit not in COUNT_UNITS:
        return None
    return NormalizedUnit(quantity=quantity, unit="count")


def compute_unit_price(total_price: float, normalized: NormalizedUnit | None) -> Optional[float]:
    """Compute unit price based on a normalized unit."""

    if not normalized or normalized.quantity == 0:
        return None
    return round(total_price / normalized.quantity, 4)

