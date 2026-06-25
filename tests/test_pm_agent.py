"""Tests for the Product Manager agent."""

from __future__ import annotations

from agents.pm_agent import ProductManagerAgent
from orchestration.state import PipelineState


def test_pm_agent_creates_spec_and_tasks():
    """PM agent should populate shared state with spec and task list."""
    state = PipelineState(
        requirement="Build a REST API with GET /health and POST /echo."
    )

    result = ProductManagerAgent().run(state)

    assert result.technical_spec is not None
    assert result.technical_spec.name
    assert result.technical_spec.description == state.requirement
    assert len(result.tasks) >= 2
    assert len(result.tasks) <= 8
    assert all(task.task_id for task in result.tasks)
    assert all(task.description for task in result.tasks)
    assert all(task.acceptance_criteria for task in result.tasks)
    assert result.status == "running"


def test_pm_agent_adds_api_task_for_api_requirement():
    """PM agent should include an API-specific task when requirement asks for API."""
    state = PipelineState(
        requirement="Build a REST API with two endpoints."
    )

    result = ProductManagerAgent().run(state)

    descriptions = [task.description.lower() for task in result.tasks]
    assert any("rest api" in description for description in descriptions)