"""File-system tools for the multi-agent development team.

The Coder and QA agents use these helpers to read and write generated source
files inside a controlled workspace directory.
"""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel


class FileToolResult(BaseModel):
    """Structured result returned by file-system tools."""

    success: bool
    path: str
    content: str | None = None
    message: str = ""


def get_workspace_root() -> Path:
    """Return the configured workspace directory and create it if needed."""
    root = Path(os.getenv("WORKSPACE_DIR", "workspace")).resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def resolve_workspace_path(path: str) -> Path:
    """Resolve a file path and ensure it stays inside the workspace."""
    root = get_workspace_root()
    requested = Path(path)

    if requested.is_absolute():
        candidate = requested.resolve()
    else:
        candidate = (root / requested).resolve()

    if candidate != root and root not in candidate.parents:
        raise ValueError(f"Path escapes workspace: {path}")

    return candidate


def read_file(path: str) -> FileToolResult:
    """Read a UTF-8 text file from the workspace.

    Args:
        path: Relative path inside the workspace.

    Returns:
        FileToolResult containing the file contents or an error message.
    """
    try:
        target = resolve_workspace_path(path)
        if not target.exists():
            return FileToolResult(
                success=False,
                path=str(target),
                message=f"File not found: {path}",
            )

        if not target.is_file():
            return FileToolResult(
                success=False,
                path=str(target),
                message=f"Path is not a file: {path}",
            )

        return FileToolResult(
            success=True,
            path=str(target),
            content=target.read_text(encoding="utf-8"),
            message="File read successfully.",
        )
    except Exception as exc:
        return FileToolResult(success=False, path=path, message=str(exc))


def write_file(path: str, content: str) -> FileToolResult:
    """Write UTF-8 text content to a workspace file.

    Args:
        path: Relative path inside the workspace.
        content: Text content to write.

    Returns:
        FileToolResult describing the write operation.
    """
    try:
        target = resolve_workspace_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        return FileToolResult(
            success=True,
            path=str(target),
            content=content,
            message="File written successfully.",
        )
    except Exception as exc:
        return FileToolResult(success=False, path=path, message=str(exc))