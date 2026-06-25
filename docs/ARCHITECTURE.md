# System Architecture

## Overview

The project implements an autonomous software engineering team using three cooperating AI agents.

```
User Requirement
        │
        ▼
Product Manager Agent
        │
Technical Specification
        │
        ▼
Coder Agent
        │
Generated Python Code
        │
        ▼
QA Agent
        │
QA Report
        │
        ▼
Completed Solution
```

---

# Components

## Product Manager Agent

Responsibilities

* Understand user requirements
* Produce technical specification
* Create implementation tasks
* Define acceptance criteria

---

## Coder Agent

Responsibilities

* Read shared state
* Generate Python code
* Execute code
* Produce implementation report

---

## QA Agent

Responsibilities

* Validate generated code
* Detect syntax issues
* Verify implementation quality
* Produce structured feedback

---

# Shared State

The agents communicate through a strongly typed `PipelineState`.

The state contains:

* Requirement
* Technical specification
* Tasks
* Generated code
* QA report
* Messages
* Runtime usage
* Cost information

---

# Runtime Layer

The runtime layer provides:

* Retry
* Circuit Breaker
* Tracing
* Cost estimation
* Usage reporting

---

# Tools

Two reusable tools are available:

* File I/O
* Sandboxed Python execution

---

# Testing

All components are tested using Pytest.

Current status:

* PM Agent
* Coder Agent
* QA Agent
* Runtime
* Pipeline
* Tools

All automated tests pass successfully.
