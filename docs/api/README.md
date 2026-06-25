# Multi-Agent Development Team API Documentation

This directory contains the generated API documentation for the multi-agent development team system.

## Overview

The multi-agent development team consists of three specialized agents that work together to solve development requirements:

- **PM Agent** (Product Manager): Analyzes requirements and creates technical specifications with task breakdowns
- **Coder Agent**: Implements solutions based on specifications
- **QA Agent**: Tests and validates the generated code

## Generated Documentation

The following modules are documented:

- **[agents](./agents/)** - Agent implementations (PM, Coder, QA)
- **[orchestration](./orchestration/)** - Pipeline orchestration and state management
- **[runtime](./runtime/)** - Runtime utilities (cost tracking, reliability, tracing)
- **[tools](./tools/)** - Tool implementations (file operations, code execution)

## Module Structure

### Agents Module
Contains the core agent implementations:
- `pm_agent.py` - Product manager agent for requirement analysis
- `coder_agent.py` - Developer agent for code generation
- `qa_agent.py` - Quality assurance agent for testing

### Orchestration Module
Manages the workflow between agents:
- `graph.py` - Main pipeline orchestration using LangGraph
- `state.py` - Shared state management between agents
- `a2a.py` - Agent-to-agent communication patterns

### Runtime Module
Provides operational utilities:
- `cost.py` - Token usage and cost tracking
- `reliability.py` - Retry logic and circuit breaker patterns
- `tracing.py` - Execution tracing and telemetry

### Tools Module
Provides tool implementations:
- `file_tools.py` - File I/O operations
- `exec_tool.py` - Python code execution

## Usage

To use the multi-agent pipeline programmatically:

```python
from orchestration.graph import MultiAgentPipeline

# Create and run the pipeline
pipeline = MultiAgentPipeline()
result = pipeline.run("Your requirement here")

# Access results
print(result.generated_code)
print(result.qa_report)
print(result.status)
```

## Command Line Usage

Run the CLI entry point:

```bash
python main.py "Your requirement here"
```

Example:
```bash
python main.py "Build a Python module that implements a binary search tree with insert, search, and in-order traversal methods."
```

## Output

The pipeline returns a comprehensive result containing:

- **requirement** - The original requirement
- **technical_spec** - Detailed technical specification created by PM Agent
- **generated_code** - Source code produced by Coder Agent
- **qa_report** - Test results and validation from QA Agent
- **status** - Overall pipeline status (completed/failed)
- **messages** - Agent communication log
- **usage** - Token and cost metrics

## Configuration

Configure the system via environment variables (see `.env.example`):

```bash
OPENAI_API_KEY=your_api_key_here
```

## See Also

- [Architecture Documentation](../ARCHITECTURE.md)
- [Reflection Report](../REFLECTION.md)
- [Test Results](../test_results.md)
