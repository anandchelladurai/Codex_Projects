"""Tests for normalization utilities."""
from app.utils.normalization import calculate_unit_price, deduplicate_results, parse_size


def test_parse_simple_size() -> None:
    size = parse_size("500 g")
    assert size.quantity == 500
    assert size.unit == "g"
    assert size.normalized_unit is not None
    assert size.normalized_unit.unit == "g"


def test_parse_multi_pack() -> None:
    size = parse_size("12x70 g")
    assert size.quantity == 840
    assert size.unit == "g"


def test_calculate_unit_price_defaults_when_unknown() -> None:
    unit_price, normalized = calculate_unit_price(6.0, "Family Pack")
    assert unit_price == 6.0
    assert normalized is None


def test_deduplicate_results() -> None:
    titles = ["Basmati Rice 5kg", "5kg basmati rice", "Chana Dal 1kg"]
    deduped = deduplicate_results(titles)
    assert len(deduped) == 2
    assert "Chana Dal 1kg" in deduped

