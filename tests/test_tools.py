"""Tests for file-system and execution tools."""

from __future__ import annotations

from tools.exec_tool import exec_python
from tools.file_tools import read_file, write_file


def test_write_and_read_file(tmp_path, monkeypatch):
    """write_file should persist content and read_file should retrieve it."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    write_result = write_file("hello.txt", "Hello Agent")
    read_result = read_file("hello.txt")

    assert write_result.success is True
    assert read_result.success is True
    assert read_result.content == "Hello Agent"


def test_read_missing_file_returns_error(tmp_path, monkeypatch):
    """read_file should return a structured error for missing files."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    result = read_file("missing.txt")

    assert result.success is False
    assert "File not found" in result.message


def test_write_file_blocks_path_escape(tmp_path, monkeypatch):
    """write_file should not allow paths outside the workspace."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    result = write_file("../evil.txt", "bad")

    assert result.success is False
    assert "escapes workspace" in result.message


def test_exec_python_success(tmp_path, monkeypatch):
    """exec_python should run a valid Python script successfully."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    write_file("script.py", "print('ok')")
    result = exec_python("script.py")

    assert result.success is True
    assert result.stdout.strip() == "ok"
    assert result.returncode == 0


def test_exec_python_timeout(tmp_path, monkeypatch):
    """exec_python should stop scripts that exceed the timeout."""
    monkeypatch.setenv("WORKSPACE_DIR", str(tmp_path))

    write_file(
        "slow.py",
        "import time\n"
        "time.sleep(2)\n"
        "print('done')\n",
    )

    result = exec_python("slow.py", timeout=1)

    assert result.success is False
    assert result.timed_out is True
    assert "timed out" in result.stderr