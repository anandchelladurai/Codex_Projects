"""Application configuration utilities."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Dict


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    try:
        return float(value) if value is not None else default
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


@dataclass
class Settings:
    """Runtime configuration loaded from environment variables."""

    live_mode: bool = field(default_factory=lambda: _env_bool("LIVE_MODE", False))
    request_timeout: float = field(default_factory=lambda: _env_float("REQUEST_TIMEOUT", 8.0))
    retry_max: int = field(default_factory=lambda: _env_int("RETRY_MAX", 2))
    rate_limit_qps: float = field(default_factory=lambda: _env_float("RATE_LIMIT_QPS", 0.5))
    cache_ttl_seconds: int = field(default_factory=lambda: _env_int("CACHE_TTL_SECONDS", 300))
    headless: bool = field(default_factory=lambda: _env_bool("HEADLESS", True))
    provider_timeouts: Dict[str, float] = field(
        default_factory=lambda: {
            "tesco": _env_float("PROVIDER_TIMEOUTS_TESCO", 8.0),
            "sainsburys": _env_float("PROVIDER_TIMEOUTS_SAINSBURYS", 8.0),
            "asda": _env_float("PROVIDER_TIMEOUTS_ASDA", 8.0),
            "morrisons": _env_float("PROVIDER_TIMEOUTS_MORRISONS", 8.0),
            "aldi": _env_float("PROVIDER_TIMEOUTS_ALDI", 8.0),
            "lidl": _env_float("PROVIDER_TIMEOUTS_LIDL", 8.0),
            "waitrose": _env_float("PROVIDER_TIMEOUTS_WAITROSE", 8.0),
            "ocado": _env_float("PROVIDER_TIMEOUTS_OCADO", 8.0),
            "iceland": _env_float("PROVIDER_TIMEOUTS_ICELAND", 8.0),
        }
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

