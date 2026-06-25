"""Binary search tree implementation."""

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
