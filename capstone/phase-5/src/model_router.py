from typing import Dict, Any
from src.config import config

class ModelRouter:
    """
    Selects the appropriate Claude model tier based on task complexity.
    Analogous to thread pool executors routing heavy vs. lightweight tasks.
    """
    @staticmethod
    def get_model_for_task(task_type: str) -> str:
        if task_type in ["intent_classification", "quick_routing", "format_check"]:
            return config.ROUTER_MODEL
        elif task_type in ["complex_reasoning", "order_investigation", "escalation_synthesis"]:
            return config.REASONING_MODEL
        else:
            # Default fallback to flagship model for safety
            return config.REASONING_MODEL