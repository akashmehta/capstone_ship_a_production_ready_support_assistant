# ADR 002: Custom Tools vs. Model Context Protocol (MCP) Server Strategy

## Status
Accepted

## 1. Custom Tool Approach (`check_local_inventory`)
* **Chosen Architecture:** Direct Python function executed in-process within the main agent runtime.
* **Justification:**
    - **Latency & Performance:** Inventory checks are high-frequency queries performed during standard customer dialogues. Running them in-process avoids IPC (inter-process communication) overhead, reducing tool-call latency to near zero.
    - **Security Hooks Integration:** Our `PreToolUse` security hooks require direct interception objects in memory. Tightly coupling local DB/inventory lookups allows deterministic hooks to inspect and drop malicious payloads instantly.

## 2. MCP Server Approach (`shipping-mcp-server`)
* **Chosen Architecture:** Standalone microservice communicating via Model Context Protocol over `stdio`.
* **Justification:**
    - **Decoupling & Sandboxing:** Carrier logistics APIs rely on third-party vendor SDKs and external network calls. Running this capability as an isolated MCP server sandboxes external network access away from the core agent application process.
    - **Reusability & Portability:** The shipping tracking capability can be reused across entirely different AI clients or future desktop apps without rewriting business logic, adhering to the standardized open MCP specification.