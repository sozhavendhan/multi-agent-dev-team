# Multi-Agent Development Team

## Overview

Multi-Agent Development Team is the final capstone project for the Saras AI Institute **Build Autonomous Multi-Agent Systems** course.

The project demonstrates an autonomous software engineering workflow where multiple AI agents collaborate to transform a natural language software requirement into executable Python code.

The system consists of three specialized agents:

* **Product Manager Agent** – converts user requirements into a structured technical specification and task breakdown.
* **Coder Agent** – generates executable Python code and executes it in a sandbox.
* **QA Agent** – validates generated code, performs static analysis, and produces structured QA reports.

The agents communicate through a shared pipeline state and follow an iterative PM → Coder → QA workflow.

---

# Features

* Multi-agent orchestration
* Shared state using Pydantic
* Agent-to-Agent (A2A) communication model
* Secure workspace file operations
* Sandboxed Python execution
* Runtime tracing
* Retry and Circuit Breaker
* Token usage and cost estimation
* Docker support
* Automated unit tests

---

# Project Structure

```text
agents/
    pm_agent.py
    coder_agent.py
    qa_agent.py

orchestration/
    state.py
    graph.py
    a2a.py

tools/
    file_tools.py
    exec_tool.py

runtime/
    reliability.py
    tracing.py
    cost.py

tests/

docs/

main.py
```

---

# Installation

```bash
git clone https://github.com/sozhavendhan/multi-agent-dev-team.git

cd multi-agent-dev-team

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

---

# Running

```bash
python main.py "Build a binary search tree implementation"
```

---

# Running Tests

```bash
python -m pytest -v
```

---

# Docker

```bash
docker compose up --build
```

---

# Technologies

* Python 3.11+
* Pydantic
* LangGraph
* ChromaDB
* Docker
* Pytest

---

# Repository

https://github.com/sozhavendhan/multi-agent-dev-team

---

# Author

Sozhavendhan

Saras AI Institute – Build Autonomous Multi-Agent Systems
