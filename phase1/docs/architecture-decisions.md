# ADR 001: Agentic vs. Fixed Boundaries and Subagent Isolation

## Status
Accepted

## Context
The Support Assistant must balance the unstructured nature of customer queries with the strict security and reliability requirements of a production enterprise system. Relying entirely on an LLM for routing, validation, and tool execution introduces unacceptable security risks (e.g., prompt injection leading to unauthorized data access) and unpredictable edge-case behavior.

## Decision 1: Fixed vs. Agentic Boundaries
We are enforcing a strict separation of concerns, similar to how we separate View logic from Repository data layers in mobile architecture.

**Fixed Workflow (Deterministic Code):**
*   **Session Management & Auth:** Verifying the user's identity token before passing any context to the agent.
*   **Pre-Tool Validation (Hooks):** Argument validation (e.g., regex checking Order IDs) and authorization checks.
*   **System Prompts & Tool Definitions:** The boundaries given to the model are immutable at runtime.
*   *Rationale:* Security, authorization, and data validation must be 100% predictable. An LLM should never be trusted to "decide" if a user has permission to view an order.

**Agentic Workflow (Probabilistic LLM):**
*   **Intent Recognition:** Parsing the customer's natural language to determine if they need general help or order specific help.
*   **Tool Selection:** Deciding *when* to trigger `lookup_order_database` based on the conversation context.
*   **Response Synthesis:** Formatting the raw JSON tool outputs into empathetic, human-readable support replies.
*   *Rationale:* LLMs excel at handling unstructured inputs and formatting outputs. We delegate the "conversation" to the agent while wrapping its "actions" in fixed code.

## Decision 2: Context Isolation via Subagents
We implemented a narrow `order_investigator` subagent rather than giving the main support agent global access to all tools.

*   **Security (Blast Radius):** The main agent cannot directly execute order lookups. If a malicious user attempts a prompt injection attack on the main agent to extract order data, the attack fails because the main agent lacks the tools.
*   **Context Window Optimization:** General product inquiries do not need instructions on how to use internal order APIs. By isolating these instructions in a subagent, we reduce prompt bloat, lower latency, and decrease token costs for 80% of standard queries.

## Decision 3: PreToolUse Security Hooks
We implemented a programmatic `PreToolUse` hook to sit between the agent's tool-call request and the actual backend API execution.

*   *Rationale:* The LLM may hallucinate an invalid Order ID format or attempt to pass unexpected arguments. The hook intercepts the payload, enforces strict regex (`^ORD-[A-Z0-9]{6}$`), and rejects bad requests *before* they consume backend resources. This treats the LLM as an untrusted client.