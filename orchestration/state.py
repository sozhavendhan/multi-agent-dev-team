"""Shared state schemas for the multi-agent development team.

The Product Manager, Coder, and QA agents all read from and write to these
models. Keeping state typed avoids ad-hoc dictionaries and makes handoffs
serializable, testable, and safe to validate before execution.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


TaskStatus = Literal["pending", "in_progress", "completed", "failed"]
AgentName = Literal["pm", "coder", "qa"]


def utc_now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


class Task(BaseModel):
    """A discrete engineering task produced by the Product Manager agent."""

    task_id: str
    description: str
    acceptance_criteria: list[str] = Field(default_factory=list)
    priority: int = Field(default=1, ge=1, le=5)
    status: TaskStatus = "pending"


class TechnicalSpec(BaseModel):
    """Structured technical specification created from the user requirement."""

    name: str
    description: str
    acceptance_criteria: list[str] = Field(default_factory=list)
    tasks: list[Task] = Field(default_factory=list)


class GeneratedCode(BaseModel):
    """Code artifact generated or revised by the Coder agent."""

    file_path: str = "generated/solution.py"
    code: str
    explanation: str = ""
    plan: list[str] = Field(default_factory=list)
    result: str = ""


class QAReport(BaseModel):
    """Result of QA test generation, execution, and failure analysis."""

    passed: bool
    tests_code: str = ""
    test_output: str = ""
    issues: list[str] = Field(default_factory=list)
    fix_instructions: list[str] = Field(default_factory=list)
    final_report: str = ""


class AgentUsage(BaseModel):
    """Per-agent token and cost tracking for one pipeline run."""

    agent_name: AgentName
    prompt_tokens: int = 0
    completion_tokens: int = 0
    estimated_cost_usd: float = 0.0
    tool_calls: int = 0
    duration_ms: int = 0


class PipelineState(BaseModel):
    """Shared workflow state passed through the orchestration graph."""

    requirement: str
    technical_spec: TechnicalSpec | None = None
    tasks: list[Task] = Field(default_factory=list)
    current_task_id: str | None = None
    generated_code: GeneratedCode | None = None
    qa_report: QAReport | None = None
    iteration: int = 0
    status: Literal["initialized", "running", "completed", "failed"] = "initialized"
    messages: list[dict[str, Any]] = Field(default_factory=list)
    usage: list[AgentUsage] = Field(default_factory=list)
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)

    def touch(self) -> None:
        """Update the state's modification timestamp."""
        self.updated_at = utc_now_iso()

    def add_message(self, sender: str, content: str) -> None:
        """Append a serializable message to the shared state."""
        self.messages.append(
            {
                "sender": sender,
                "content": content,
                "timestamp": utc_now_iso(),
            }
        )
        self.touch()

    def set_task_status(self, task_id: str, status: TaskStatus) -> None:
        """Update the status of a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = status
                self.touch()
                return
        raise ValueError(f"Task not found: {task_id}")