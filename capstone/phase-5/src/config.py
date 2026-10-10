os
from pydantic import BaseModel, Field

class AppConfig(BaseModel):
    """
    Tiered model configuration for cost-defensible enterprise scaling.
    """
    # Fast, cost-efficient model for high-frequency classification and routing
    ROUTER_MODEL: str = Field(default="claude-3-5-haiku-20241022", description="Fast model for intent parsing")

    # High-capability model for complex multi-turn reasoning and tool use
    REASONING_MODEL: str = Field(default="claude-3-5-sonnet-20241022", description="Flagship model for core agent")

    # Caching configuration
    ENABLE_PROMPT_CACHING: bool = Field(default=True, description="Toggle ephemeral prompt caching")

    ANTHROPIC_API_KEY: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))

config = AppConfig()