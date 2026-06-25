"""Simple PM -> Coder -> QA orchestration graph."""

from __future__ import annotations

from agents.coder_agent import CoderAgent
from agents.pm_agent import ProductManagerAgent
from agents.qa_agent import QAAgent
from orchestration.state import PipelineState


class MultiAgentPipeline:
    """Coordinates PM, Coder, and QA agents."""

    def __init__(self, max_iterations: int = 5):
        self.pm = ProductManagerAgent()
        self.coder = CoderAgent()
        self.qa = QAAgent()
        self.max_iterations = max_iterations

    def run(self, requirement: str) -> PipelineState:
        """Run the complete workflow."""
        state = PipelineState(requirement=requirement)

        state = self.pm.run(state)

        for iteration in range(self.max_iterations):
            state.iteration = iteration + 1

            state = self.coder.run(state)
            state = self.qa.run(state)

            if state.qa_report and state.qa_report.passed:
                state.status = "completed"
                return state

        state.status = "failed"

        if state.qa_report:
            state.qa_report.final_report = (
                f"Failed after {self.max_iterations} iterations."
            )

        return state