import re
import logging
from claude_agent_sdk.hooks import PreToolUseHook, HookContext, HookResult

logger = logging.getLogger(__name__)

class OrderSecurityHook(PreToolUseHook):
    """
    Intercepts tool calls before execution to enforce business rules
    and security boundaries deterministically.
    """
    def pre_tool_use(self, context: HookContext, tool_name: str, tool_input: dict) -> HookResult:
        # We only care about intercepting the lookup_order tool
        if tool_name == "lookup_order":
            order_id = tool_input.get("order_id", "")

            # Deterministic Regex check: Orders must follow format 'ORD-XXXXXX'
            if not re.match(r"^ORD-[A-Z0-9]{6}$", order_id):
                logger.warning(f"Blocked invalid order ID lookup attempt: {order_id}")

                # Rejecting at the hook level prevents the tool from running
                # and feeds this exact error message back into the Claude context
                return HookResult.reject(
                    reason="System rejection: order_id must follow the format 'ORD-' followed by 6 alphanumeric characters."
                )

        # Allow all other tools or valid inputs to pass through
        return HookResult.proceed()