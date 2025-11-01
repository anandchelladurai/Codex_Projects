"""Parsing helpers for provider payloads."""
from __future__ import annotations

import re
from typing import Iterable, List

BRAND_REGEX = re.compile(r"\b(tilda|laila|trs|heera|east end|maggi|mdh|aashirvaad|patak's|shan|ashoka)\b", re.I)


def tokenize(text: str) -> List[str]:
    """Simple tokenizer returning lowercase words."""

    return re.findall(r"[a-z0-9]+", text.lower())


def fuzzy_contains(query_tokens: Iterable[str], text: str) -> bool:
    """Check whether all query tokens appear in the text."""

    text_tokens = set(tokenize(text))
    return all(token in text_tokens for token in query_tokens)


def has_indian_brand(text: str) -> bool:
    """Return whether text appears to contain a known Indian brand."""

    return bool(BRAND_REGEX.search(text))

