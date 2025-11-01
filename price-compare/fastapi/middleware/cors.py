"""Stub CORS middleware for compatibility."""
from __future__ import annotations


class CORSMiddleware:  # pragma: no cover - passive stub
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

