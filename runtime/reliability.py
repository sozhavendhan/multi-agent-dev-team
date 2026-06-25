"""Reliability utilities: retry and circuit breaker."""

from __future__ import annotations

import functools
import logging
import random
import time
from typing import Any, Callable

logger = logging.getLogger(__name__)


def retry(max_retries: int = 3, base_delay: float = 0.2) -> Callable:
    """Retry a function with exponential backoff and jitter."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_error = exc
                    sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            raise last_error
        return wrapper
    return decorator


class CircuitBreaker:
    """Simple circuit breaker with closed, open, and half-open states."""

    def __init__(self, failure_threshold: int = 3, cooldown_seconds: int = 30):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.failure_count = 0
        self.state = "closed"
        self.opened_at: float | None = None

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Call a function through the circuit breaker."""
        if self.state == "open":
            if self.opened_at and time.time() - self.opened_at >= self.cooldown_seconds:
                self.state = "half-open"
                logger.warning("Circuit breaker moved to half-open.")
            else:
                raise RuntimeError("Circuit breaker is open.")

        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            self.state = "closed"
            return result
        except Exception:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                self.opened_at = time.time()
                logger.warning("Circuit breaker opened after failures.")
            raise