import os
from claude_agent_sdk import ClaudeAgent, AgentOptions
from src.config import config
from src.hooks import SecurityHooks
from src.tools.order_tools import lookup_order_database, fetch_tracking_api
from src.tools.kb_tools import search_knowledge_base
from src.tools.escalation_tools import escalate_to_human
from src.prompts.v1_support_prompt import SYSTEM_PROMPT_V1

def initialize_support_agent() -> ClaudeAgent:
    """
    Initializes the support agent with pinned models and prompt caching headers.
    """
    # Construct system prompt with ephemeral cache control for cost optimization
    system_prompt_block = [
        {
            "type": "text",
            "text": SYSTEM_PROMPT_V1,
            # Prompt Caching: Instruct Anthropic API to cache this static block
            "cache_control": {"type": "ephemeral"} if config.ENABLE_PROMPT_CACHING else None
        }
    ]

    options = AgentOptions(
        model=config.REASONING_MODEL,
        system_prompt=system_prompt_block,
        tools=[lookup_order_database, fetch_tracking_api, search_knowledge_base, escalate_to_human],
        permission_mode="strict"
    )

    agent = ClaudeAgent(api_key=config.ANTHROPIC_API_KEY, options=options)
    agent.register_hook("pre_tool_use", SecurityHooks.pre_tool_use_hook)

    return agent