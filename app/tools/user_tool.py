from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parents[2]
USERS_FILE = BASE_DIR / "data" / "users.json"


class UpdateAddressTool:
    """Utility for updating user addresses in users.json."""

    def __init__(self, data_file: Path | None = None) -> None:
        self._data_file = data_file or USERS_FILE

    def _load_users(self) -> List[Dict[str, Any]]:
        if not self._data_file.exists():
            raise FileNotFoundError(f"Users file not found: {self._data_file}")
        with self._data_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _save_users(self, users: List[Dict[str, Any]]) -> None:
        with self._data_file.open("w", encoding="utf-8") as handle:
            json.dump(users, handle, indent=2)

    def update(self, user_id: str, new_address: str) -> Dict[str, Any]:
        """Update user address and save to users.json."""
        try:
            users = self._load_users()
        except FileNotFoundError as exc:
            return {"error": str(exc)}

        for user in users:
            if user.get("user_id") == user_id:
                user["address"] = new_address
                self._save_users(users)
                return user

        return {"error": f"User '{user_id}' not found."}

