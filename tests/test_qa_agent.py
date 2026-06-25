"""Tests for QA Agent."""

from __future__ import annotations

from agents.coder_agent import CoderAgent
from agents.pm_agent import ProductManagerAgent
from agents.qa_agent import QAAgent
from orchestration.state import PipelineState


def test_qa_agent_passes_generated_code(tmp_path, monkeypatch):
    """QA should accept valid generated code."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    state = PipelineState(requirement="Print hello world.")
    state = ProductManagerAgent().run(state)
    state = CoderAgent().run(state)
    state = QAAgent().run(state)

    assert state.qa_report is not None
    assert state.qa_report.passed is True


def test_qa_agent_detects_missing_main_guard():
    """QA should detect missing main guard."""
    state = PipelineState(requirement="test")
    state.generated_code = type(
        "GeneratedCode",
        (),
        {
            "code": "print('hello')",
        },
    )()

    state = QAAgent().run(state)

    assert state.qa_report is not None
    assert state.qa_report.passed is False
    assert "Missing main guard." in state.qa_report.issues