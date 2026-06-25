"""QA and Debugger agent."""

from __future__ import annotations

import ast

from orchestration.state import PipelineState, QAReport


class QAAgent:
    """Reviews generated code and produces structured fix instructions."""

    def run(self, state: PipelineState) -> PipelineState:
        """Review generated code and populate the QA report."""
        if state.generated_code is None:
            raise ValueError("No generated code found.")

        code = state.generated_code.code

        issues = self._find_issues(code)
        passed = len(issues) == 0

        state.qa_report = QAReport(
            passed=passed,
            issues=issues,
            fix_instructions=issues,
            final_report="All tests passed." if passed else "Issues found.",
        )

        state.add_message(
            "qa",
            "QA review passed."
            if passed
            else f"QA review found {len(issues)} issues."
        )

        return state

    def _find_issues(self, code: str) -> list[str]:
        """Run lightweight static checks."""
        issues = []

        try:
            ast.parse(code)
        except SyntaxError as exc:
            issues.append(f"Syntax error: {exc}")

        if "if __name__ == \"__main__\"" not in code:
            issues.append("Missing main guard.")

        if "TODO" in code:
            issues.append("Contains TODO placeholder.")

        return issues