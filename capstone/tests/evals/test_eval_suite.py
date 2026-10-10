import pytest
from src.hooks import SecurityHooks

def test_hook_valid_order_id():
    """Verify PreToolUse hook allows valid ORD-XXXXXX inputs."""
    valid_input = {"order_id": "ORD-100200"}
    result = SecurityHooks.pre_tool_use_hook("lookup_order_database", valid_input)
    assert result == valid_input

def test_hook_invalid_order_id_rejection():
    """Verify PreToolUse hook intercepts invalid or malicious Order IDs."""
    invalid_input = {"order_id": "ORD-123'; DROP TABLE Orders;--"}
    with pytest.raises(ValueError) as exc_info:
        SecurityHooks.pre_tool_use_hook("lookup_order_database", invalid_input)
    assert "Invalid Order ID format" in str(exc_info.value)

def test_hook_admin_access_prevention():
    """Verify PreToolUse hook blocks access to restricted records."""
    admin_input = {"order_id": "ORD-ADMIN1"}
    with pytest.raises(PermissionError):
        SecurityHooks.pre_tool_use_hook("lookup_order_database", admin_input)
