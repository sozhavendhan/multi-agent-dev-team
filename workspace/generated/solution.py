"""Word frequency command-line tool."""

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
