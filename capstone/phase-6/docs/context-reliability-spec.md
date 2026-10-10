# Phase 6: Prompt & Context Reliability Specification

## 1. Context Pruning & Compaction Strategy
* **The Problem:** As customer support dialogues stretch past 15-20 turns, LLMs experience context degradation, frequently forgetting core system prompt instructions or hallucinating previous state details.
* **The Solution:** Our `SessionManager` enforces a hard sliding window capped at 10 active turns (20 messages). Additionally, any single message exceeding 1,500 characters is programmatically truncated to preserve prompt clarity and keep API token latency minimal.

## 2. Defensive Parsing & Structured Output
* **The Problem:** Downstream ticketing systems and analytics pipelines fail when LLM tool parameters or JSON responses contain unexpected types, missing fields, or invalid schemas.
* **The Solution:** All critical tool outputs (such as `escalate_to_human`) pass through strict Pydantic validation models (`EscalationTicketSchema`). If an invalid payload is detected, a graceful error dictionary is returned to the model loop rather than raising an unhandled application exception.