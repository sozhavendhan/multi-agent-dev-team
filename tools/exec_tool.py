"""Sandboxed Python execution tool.

This module executes generated Python files in a subprocess with timeout
protection. It intentionally avoids eval(), exec(), and shell=True.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

from pydantic import BaseModel, Field

from tools.file_tools import resolve_workspace_path


class ExecResult(BaseModel):
    """Structured result returned by the Python execution tool."""

    success: bool
    path: str
    stdout: str = ""
    stderr: str = ""
    returncode: int | None = None
    timed_out: bool = False
    duration_ms: int = 0
    command: list[str] = Field(default_factory=list)


def exec_python(
    path: str,
    timeout: int | None = None,
    args: list[str] | None = None,
) -> ExecResult:
    """Execute a Python file in a subprocess with a timeout.

    Args:
        path: Relative Python file path inside the workspace.
        timeout: Optional timeout in seconds. Defaults to EXEC_TIMEOUT_SECONDS.
        args: Optional command-line arguments passed to the Python script.

    Returns:
        ExecResult with stdout, stderr, return code, timeout flag, and duration.
    """
    timeout_seconds = timeout or int(os.getenv("EXEC_TIMEOUT_SECONDS", "10"))
    script_args = args or []

    start = time.perf_counter()

    try:
        target = resolve_workspace_path(path)

        if not target.exists():
            return ExecResult(
                success=False,
                path=str(target),
                stderr=f"Python file not found: {path}",
                duration_ms=_duration_ms(start),
            )

        if target.suffix != ".py":
            return ExecResult(
                success=False,
                path=str(target),
                stderr=f"Only .py files can be executed: {path}",
                duration_ms=_duration_ms(start),
            )

        command = [sys.executable, str(target), *script_args]

        completed = subprocess.run(
            command,
            cwd=str(target.parent),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            shell=False,
            check=False,
        )

        return ExecResult(
            success=completed.returncode == 0,
            path=str(target),
            stdout=completed.stdout,
            stderr=completed.stderr,
            returncode=completed.returncode,
            timed_out=False,
            duration_ms=_duration_ms(start),
            command=command,
        )

    except subprocess.TimeoutExpired as exc:
        return ExecResult(
            success=False,
            path=path,
            stdout=exc.stdout or "",
            stderr=f"Execution timed out after {timeout_seconds} seconds.",
            returncode=None,
            timed_out=True,
            duration_ms=_duration_ms(start),
            command=[sys.executable, path, *script_args],
        )
    except Exception as exc:
        return ExecResult(
            success=False,
            path=path,
            stderr=str(exc),
            duration_ms=_duration_ms(start),
        )


def _duration_ms(start: float) -> int:
    """Return elapsed milliseconds since a perf_counter start value."""
    return int((time.perf_counter() - start) * 1000)