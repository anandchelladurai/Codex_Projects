"""Tests for unit normalization helpers."""
from app.utils.units import NormalizedUnit, compute_unit_price, normalize_count, normalize_volume, normalize_weight


def test_normalize_weight_kg_to_g() -> None:
    normalized = normalize_weight(2, "kg")
    assert normalized == NormalizedUnit(quantity=2000, unit="g")


def test_normalize_volume_l_to_ml() -> None:
    normalized = normalize_volume(1.5, "l")
    assert normalized == NormalizedUnit(quantity=1500, unit="ml")


def test_normalize_count() -> None:
    normalized = normalize_count(6, "count")
    assert normalized == NormalizedUnit(quantity=6, unit="count")


def test_compute_unit_price() -> None:
    normalized = NormalizedUnit(quantity=1000, unit="g")
    price = compute_unit_price(4.5, normalized)
    assert price == 0.0045

