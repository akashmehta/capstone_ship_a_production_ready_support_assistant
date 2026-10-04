import os
from typing import Dict, Any
from pydantic import BaseModel, Field

class AppConfig(BaseModel):
    """
    Central configuration with strict model pinning and environment settings.
    """
    # Model Pinning: Exact snapshot to prevent unexpected behavioral changes
    PRIMARY_MODEL: str = Field(default="claude-3-5-sonnet-20241022", description="Pinned Claude model version")
    SUBAGENT_MODEL: str = Field(default="claude-3-5-sonnet-20241022", description="Pinned model for subagents")

    # Context & Session Settings
    MAX_HISTORY_TURNS: int = Field(default=10, description="Max conversation turns preserved in sliding window")
    MAX_TOKENS_PER_RESPONSE: int = Field(default=1024, description="Max completion token count")

    # API Keys
    ANTHROPIC_API_KEY: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))

    def validate_environment(self) -> None:
        if not self.ANTHROPIC_API_KEY:
            raise ValueError("CRITICAL: ANTHROPIC_API_KEY is missing from environment variables.")

config = AppConfig()