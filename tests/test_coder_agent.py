"""Tests for the Coder agent."""

from __future__ import annotations

from agents.coder_agent import CoderAgent
from agents.pm_agent import ProductManagerAgent
from orchestration.state import PipelineState


def test_coder_agent_generates_executable_code(tmp_path, monkeypatch):
    """Coder should generate, write, and execute Python code."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    state = PipelineState(requirement="Print hello world.")
    state = ProductManagerAgent().run(state)

    result = CoderAgent().run(state)

    assert result.generated_code is not None
    assert "Generated solution" in result.generated_code.code
    assert "successfully" in result.generated_code.result
    assert all(task.status == "completed" for task in result.tasks)


def test_coder_agent_generates_bst_code(tmp_path, monkeypatch):
    """Coder should generate BST code for the Week 4 grading task."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    state = PipelineState(
        requirement="Build a Python module that implements a binary search tree."
    )
    state = ProductManagerAgent().run(state)

    result = CoderAgent().run(state)

    assert result.generated_code is not None
    assert "class BinarySearchTree" in result.generated_code.code
    assert result.generated_code.result == ""


def test_self_reflection_returns_no_issues_for_modular_code():
    """Self-reflection should accept modular code with a main guard."""
    code = 'def main():\\n    pass\\n\\nif __name__ == "__main__":\\n    main()\\n'

    issues = CoderAgent().self_reflect(code)

    assert issues == ["No issues found."]