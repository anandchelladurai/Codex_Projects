"""Simple TTL cache for search results."""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class TTLCache:
    """A minimal TTL cache suitable for this application."""

    def __init__(self, ttl_seconds: int) -> None:
        self.ttl_seconds = ttl_seconds
        self._store: Dict[str, CacheEntry] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if not entry:
            return None
        if entry.expires_at < time.time():
            del self._store[key]
            return None
        return entry.value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = CacheEntry(value=value, expires_at=time.time() + self.ttl_seconds)

    def clear(self) -> None:
        self._store.clear()


def make_cache_key(*parts: str) -> str:
    return "::".join(parts)

