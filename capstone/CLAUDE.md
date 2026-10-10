# Development & AI Collaboration Guidelines (CLAUDE.md)

## Repo Overview
Python-based Claude Support Assistant using the Claude Agent SDK, Pydantic schemas, and strict tool hooks.

## Environment & Build Rules
- Python Version: 3.11+
- Virtual Environment: `.venv`
- Install Dependencies: `pip install -r requirements.txt`
- Run Tests: `pytest tests/`

## Coding Standards
1. **Explicit Type Hinting:** All functions must have full type annotations.
2. **Pydantic Validation:** Inputs, outputs, and tool schemas must inherit from `pydantic.BaseModel`.
3. **Model Pinning:** Never use mutable model aliases like `claude-3-5-sonnet`. Always use explicit release snapshots (e.g., `claude-3-5-sonnet-20241022` or `claude-3-7-sonnet-20250219`).
4. **Error Handling:** Never swallow LLM API exceptions. Standardize responses via `APIResponseEnvelope`.

## Allowed Commands for Claude Code CLI
- `pytest tests/`
- `flake8 src/`
- `black --check src/`

# Support Assistant - Claude Code Developer Guide & Architecture

## System Architecture Overview
The Support Assistant is a hybrid system built with Python 3.11+ and the Claude Agent SDK.

* **Fixed Workflow (Deterministic):** Session management, pre-tool hook security checks (`src/hooks.py`), Pydantic validation (`src/models/schema.py`), and error envelopes.
* **Agentic Workflow (Probabilistic):** Dynamic intent parsing, contextual tool invocation, and natural language formatting (`src/agent.py`).
* **Subagent Context Isolation:** Order queries are delegated to `.claude/agents/order-investigator.md` to prevent PII exposure and context window bloat.

## Essential Developer Commands

### Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt