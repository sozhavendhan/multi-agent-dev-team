"""Token and cost reporting utilities."""

from __future__ import annotations

import json
from pathlib import Path

from orchestration.state import AgentUsage, PipelineState


MODEL_PRICES_PER_1K = {
    "gpt-4o": 0.005,
    "gpt-4o-mini": 0.00015,
}


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Estimate cost from model and token counts."""
    price = MODEL_PRICES_PER_1K.get(model, 0.00015)
    return round(((prompt_tokens + completion_tokens) / 1000) * price, 6)


def add_usage(
    state: PipelineState,
    agent_name: str,
    prompt_tokens: int,
    completion_tokens: int,
    model: str,
    tool_calls: int = 0,
    duration_ms: int = 0,
) -> PipelineState:
    """Append usage data to pipeline state."""
    state.usage.append(
        AgentUsage(
            agent_name=agent_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost_usd=estimate_cost(model, prompt_tokens, completion_tokens),
            tool_calls=tool_calls,
            duration_ms=duration_ms,
        )
    )
    return state


def write_cost_report(state: PipelineState, path: str = "docs/cost_reports/latest.json") -> str:
    """Write a JSON cost report for a pipeline run."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    total = round(sum(item.estimated_cost_usd for item in state.usage), 6)

    payload = {
        "requirement": state.requirement,
        "status": state.status,
        "iterations": state.iteration,
        "agents": [item.model_dump() for item in state.usage],
        "total_estimated_cost_usd": total,
    }

    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(target)