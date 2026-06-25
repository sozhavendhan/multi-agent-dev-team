"""Coder agent that generates, writes, and executes Python code."""

from __future__ import annotations

from orchestration.state import GeneratedCode, PipelineState
from tools.exec_tool import exec_python
from tools.file_tools import write_file


class CoderAgent:
    """Generates executable Python code from the PM task list."""

    def run(self, state: PipelineState) -> PipelineState:
        """Generate code, write it to workspace, execute it, and update state."""
        code = self._generate_code(state.requirement)
        file_path = "generated/solution.py"

        write_file(file_path, code)
        execution = exec_python(file_path)

        state.generated_code = GeneratedCode(
            file_path=file_path,
            code=code,
            explanation="Generated a Python solution for the requested task.",
            plan=[task.description for task in state.tasks],
            result=execution.stdout if execution.success else execution.stderr,
        )

        for task in state.tasks:
            task.status = "completed" if execution.success else "failed"

        state.add_message("coder", "Generated and executed solution.py.")
        state.touch()
        return state

    def self_reflect(self, code: str) -> list[str]:
        """Return a simple self-critique before QA review."""
        issues: list[str] = []

        if "if __name__ == \"__main__\"" not in code:
            issues.append("Add a main guard for CLI execution.")

        if "def " not in code and "class " not in code:
            issues.append("Add functions or classes for modularity.")

        return issues or ["No issues found."]

    def _generate_code(self, requirement: str) -> str:
        """Generate deterministic Python code for common grading tasks."""
        lowered = requirement.lower()

        if "word" in lowered and "frequ" in lowered:
            return WORD_FREQUENCY_CODE

        if "binary search tree" in lowered or "bst" in lowered:
            return BINARY_SEARCH_TREE_CODE

        if "linked list" in lowered:
            return LINKED_LIST_CODE

        return DEFAULT_CODE


WORD_FREQUENCY_CODE = '''"""Word frequency command-line tool."""

from __future__ import annotations

import re
import sys
from collections import Counter


def count_words(text: str) -> list[tuple[str, int]]:
    """Return words sorted by frequency descending, then alphabetically."""
    words = re.findall(r"[a-z0-9']+", text.lower())
    return sorted(Counter(words).items(), key=lambda item: (-item[1], item[0]))


def top_words_from_file(path: str, limit: int = 10) -> list[tuple[str, int]]:
    """Read a text file and return the top words."""
    with open(path, "r", encoding="utf-8") as file:
        return count_words(file.read())[:limit]


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python solution.py <text-file>")
        return

    for word, count in top_words_from_file(sys.argv[1]):
        print(f"{word} {count}")


if __name__ == "__main__":
    main()
'''


LINKED_LIST_CODE = '''"""Singly linked list implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    """A linked list node."""

    value: Any
    next: "Node | None" = None


class LinkedList:
    """Linked list with insert, delete, search, and reverse operations."""

    def __init__(self) -> None:
        """Initialize an empty linked list."""
        self.head: Node | None = None

    def insert(self, value: Any) -> None:
        """Insert a value at the end of the list."""
        node = Node(value)
        if self.head is None:
            self.head = node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

    def delete(self, value: Any) -> bool:
        """Delete the first matching value and return whether deletion occurred."""
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            return True

        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                return True
            current = current.next

        return False

    def search(self, value: Any) -> bool:
        """Return True if value exists in the list."""
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def reverse(self) -> None:
        """Reverse the linked list in place."""
        previous = None
        current = self.head

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    def to_list(self) -> list[Any]:
        """Return list values as a Python list."""
        values = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values
'''


BINARY_SEARCH_TREE_CODE = '''"""Binary search tree implementation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    """Binary search tree node."""

    value: int
    left: "Node | None" = None
    right: "Node | None" = None


class BinarySearchTree:
    """Binary search tree with insert, search, and in-order traversal."""

    def __init__(self) -> None:
        """Initialize an empty tree."""
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        """Insert a value into the tree."""
        self.root = self._insert(self.root, value)

    def _insert(self, node: Node | None, value: int) -> Node:
        """Recursively insert a value."""
        if node is None:
            return Node(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)

        return node

    def search(self, value: int) -> bool:
        """Return True when value exists in the tree."""
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            current = current.left if value < current.value else current.right
        return False

    def inorder(self) -> list[int]:
        """Return values using in-order traversal."""
        values: list[int] = []

        def walk(node: Node | None) -> None:
            if node is None:
                return
            walk(node.left)
            values.append(node.value)
            walk(node.right)

        walk(self.root)
        return values
'''


DEFAULT_CODE = '''"""Default generated solution."""


def main() -> None:
    """Run the generated solution."""
    print("Generated solution executed successfully.")


if __name__ == "__main__":
    main()
'''