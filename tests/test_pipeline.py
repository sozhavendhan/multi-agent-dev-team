"""Tests for the end-to-end multi-agent pipeline."""

from __future__ import annotations

from orchestration.graph import MultiAgentPipeline


def test_pipeline_completes_successfully(tmp_path, monkeypatch):
    """Pipeline should complete successfully."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    pipeline = MultiAgentPipeline()

    result = pipeline.run("Print hello world.")

    assert result.status == "completed"
    assert result.qa_report is not None
    assert result.qa_report.passed is True