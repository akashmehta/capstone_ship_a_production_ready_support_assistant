import os
from claude_agent_sdk import AgentClient, AgentConfig
from tools.order_tools import lookup_order, check_inventory
from hooks import OrderSecurityHook

def build_support_agent() -> AgentClient:
    """
    Constructs the production Claude support agent, wiring in tools,
    subagents, and lifecycle hooks.
    """
    # Initialize the client with our baseline configuration
    config = AgentConfig(
        model="claude-3-5-sonnet-20241022",
        temperature=0.2, # Low temperature for support reliability
        agents_dir=os.path.join(os.getcwd(), ".claude", "agents")
    )

    agent = AgentClient(config=config)

    # Register our deterministic security hooks
    agent.register_hook(OrderSecurityHook())

    # Register tools that the main agent or subagents might need
    agent.register_tools([lookup_order, check_inventory])

    return agent

if __name__ == "__main__":
    support_assistant = build_support_agent()
    # Ready to be imported and consumed by our routing layer