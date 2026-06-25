"""Product Manager agent for requirement decomposition."""

from __future__ import annotations

import re

from orchestration.state import PipelineState, Task, TechnicalSpec


class ProductManagerAgent:
    """Creates a structured technical specification from a user requirement."""

    def run(self, state: PipelineState) -> PipelineState:
        """Populate shared state with a technical spec and task list."""
        tasks = self._build_tasks(state.requirement)

        spec = TechnicalSpec(
            name=self._make_name(state.requirement),
            description=state.requirement,
            acceptance_criteria=[
                "Generated code satisfies the original requirement.",
                "Code is executable Python.",
                "QA tests pass successfully.",
            ],
            tasks=tasks,
        )

        state.technical_spec = spec
        state.tasks = tasks
        state.status = "running"
        state.add_message("pm", f"Created technical spec with {len(tasks)} tasks.")
        return state

    def _make_name(self, requirement: str) -> str:
        """Create a short project name from the requirement."""
        words = re.findall(r"[A-Za-z0-9]+", requirement.lower())[:6]
        return "-".join(words) or "generated-project"

    def _build_tasks(self, requirement: str) -> list[Task]:
        """Create up to eight implementation tasks from a requirement."""
        base_tasks = [
            Task(
                task_id="task-1",
                description="Analyze the requirement and identify the expected module interface.",
                acceptance_criteria=["Expected classes, functions, or endpoints are clear."],
                priority=1,
            ),
            Task(
                task_id="task-2",
                description="Implement the core Python solution.",
                acceptance_criteria=["Implementation satisfies the primary behavior."],
                priority=1,
            ),
            Task(
                task_id="task-3",
                description="Add input validation and edge-case handling.",
                acceptance_criteria=["Invalid inputs are handled safely."],
                priority=2,
            ),
            Task(
                task_id="task-4",
                description="Run generated code and capture execution results.",
                acceptance_criteria=["Generated code executes without syntax errors."],
                priority=2,
            ),
        ]

        if "api" in requirement.lower() or "endpoint" in requirement.lower():
            base_tasks.insert(
                2,
                Task(
                    task_id="task-api",
                    description="Implement requested REST API endpoints.",
                    acceptance_criteria=["All requested endpoints return expected responses."],
                    priority=1,
                ),
            )

        return base_tasks[:8]