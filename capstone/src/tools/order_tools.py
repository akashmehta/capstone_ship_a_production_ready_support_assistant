import json
from typing import Dict, Any

def lookup_order_database(order_id: str) -> str:
    """
    Retrieves order details from the backend database by Order ID.
    Fixed schema output to match API Response requirements.
    """
    mock_db: Dict[str, Dict[str, Any]] = {
        "ORD-100200": {
            "order_status": "SHIPPED",  # Fixed: Key aligned with schema spec
            "items": ["Wireless Noise-Canceling Headphones"],
            "carrier": "FedEx",
            "tracking_number": "FX987654321"
        }
    }

    order = mock_db.get(order_id)
    if not order:
        return json.dumps({
            "order_status": "NOT_FOUND",
            "error": f"Order '{order_id}' was not found in the system."
        })
    return json.dumps(order)