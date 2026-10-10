# in-process tool for querying local warehouse stock levels.
import json
from typing import Dict, Any

def check_local_inventory(sku: str) -> str:
    """
    Custom Tool: Checks real-time warehouse inventory for a given product SKU.
    Runs directly in-process for minimal latency and tight hook enforcement.
    """
    warehouse_stock: Dict[str, Dict[str, Any]] = {
        "SKU-HEADPHONE-01": {"in_stock": True, "quantity": 142, "warehouse": "Chicago-WH1"},
        "SKU-WATCH-05": {"in_stock": False, "quantity": 0, "warehouse": "Dallas-WH2"},
        "SKU-DOCK-99": {"in_stock": True, "quantity": 28, "warehouse": "Seattle-WH3"}
    }

    item = warehouse_stock.get(sku.upper())
    if not item:
        return json.dumps({"error": f"SKU '{sku}' not recognized in inventory catalog."})
    return json.dumps(item)