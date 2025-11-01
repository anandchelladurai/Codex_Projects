"""Shared helpers for providers."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from ..utils import parsing

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> List[dict]:
    """Load a fixture JSON file."""

    path = FIXTURE_DIR / f"{name}.json"
    return json.loads(path.read_text())


def filter_by_query(data: Iterable[dict], query: str) -> List[dict]:
    """Filter fixture data by query tokens."""

    tokens = parsing.tokenize(query)
    if not tokens:
        return list(data)
    filtered = [item for item in data if parsing.fuzzy_contains(tokens, item["title"])]
    return filtered or list(data)

