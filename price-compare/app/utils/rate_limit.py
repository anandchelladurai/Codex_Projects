"""Token bucket rate limiter."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass


@dataclass
class TokenBucket:
    capacity: float
    tokens: float
    fill_rate: float
    last_checked: float

    def consume(self, amount: float) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_checked
        self.last_checked = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False


class RateLimiter:
    """Thread-safe token bucket rate limiter."""

    def __init__(self, qps: float) -> None:
        capacity = max(qps, 1.0)
        self.bucket = TokenBucket(capacity=capacity, tokens=capacity, fill_rate=qps, last_checked=time.monotonic())
        self._lock = threading.Lock()

    def acquire(self, amount: float = 1.0, timeout: float = 5.0) -> bool:
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            with self._lock:
                if self.bucket.consume(amount):
                    return True
            time.sleep(0.05)
        return False

