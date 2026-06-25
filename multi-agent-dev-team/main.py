"""CLI entry point for the final multi-agent development team."""

from __future__ import annotations

import argparse
import json

from orchestration.graph import MultiAgentPipeline


def main() -> None:
    """Run the multi-agent pipeline from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "requirement",
        nargs="?",
        default="Build a Python module that implements a binary search tree with insert, search, and in-order traversal methods.",
    )
    args = parser.parse_args()

    result = MultiAgentPipeline().run(args.requirement)

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()