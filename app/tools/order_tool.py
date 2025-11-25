from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parents[2]
ORDERS_FILE = BASE_DIR / "data" / "orders.json"


class OrderLookupTool:
    """Lookup tool backed by the local orders.json file."""

    def __init__(self, data_file: Path | None = None) -> None:
        self._data_file = data_file or ORDERS_FILE

    def _load_orders(self) -> List[Dict[str, Any]]:
        if not self._data_file.exists():
            raise FileNotFoundError(f"Orders file not found: {self._data_file}")
        with self._data_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def lookup(self, order_id: str) -> Dict[str, Any]:
        """Return order details or an error message."""
        try:
            orders = self._load_orders()
        except FileNotFoundError as exc:
            return {"error": str(exc)}

        for order in orders:
            if order.get("order_id") == order_id:
                return order

        return {"error": f"Order '{order_id}' not found."}

