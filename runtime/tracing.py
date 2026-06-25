"""Local tracing helpers for agent runs."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def trace_span(agent_name: str, metadata: dict | None = None) -> Iterator[dict]:
    """Create a local trace span with timing metadata."""
    start = time.perf_counter()
    span = {
        "agent_name": agent_name,
        "metadata": metadata or {},
        "duration_ms": 0,
    }

    try:
        yield span
    finally:
        span["duration_ms"] = int((time.perf_counter() - start) * 1000)