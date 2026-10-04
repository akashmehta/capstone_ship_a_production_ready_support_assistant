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