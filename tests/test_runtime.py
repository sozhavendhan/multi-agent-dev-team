"""Tests for runtime production-readiness utilities."""

from __future__ import annotations

import pytest

from orchestration.state import PipelineState
from runtime.cost import add_usage, estimate_cost, write_cost_report
from runtime.reliability import CircuitBreaker, retry
from runtime.tracing import trace_span


def test_retry_eventually_succeeds():
    """retry should call a flaky function again until it succeeds."""
    calls = {"count": 0}

    @retry(max_retries=3, base_delay=0)
    def flaky():
        calls["count"] += 1
        if calls["count"] < 2:
            raise ValueError("temporary")
        return "ok"

    assert flaky() == "ok"
    assert calls["count"] == 2


def test_circuit_breaker_opens_after_failures():
    """circuit breaker should open after configured failures."""
    breaker = CircuitBreaker(failure_threshold=2, cooldown_seconds=30)

    def fail():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        breaker.call(fail)

    with pytest.raises(RuntimeError):
        breaker.call(fail)

    assert breaker.state == "open"


def test_cost_report_written(tmp_path):
    """cost report should be written as JSON."""
    state = PipelineState(requirement="test")
    state = add_usage(
        state,
        agent_name="pm",
        prompt_tokens=100,
        completion_tokens=50,
        model="gpt-4o",
    )

    report_path = write_cost_report(state, str(tmp_path / "cost.json"))

    assert report_path.endswith("cost.json")
    assert estimate_cost("gpt-4o", 100, 50) > 0


def test_trace_span_records_duration():
    """trace span should record duration."""
    with trace_span("pm") as span:
        assert span["agent_name"] == "pm"

    assert span["duration_ms"] >= 0