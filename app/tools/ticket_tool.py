from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parents[2]
TICKETS_FILE = BASE_DIR / "data" / "tickets.json"


class TicketTool:
    """Simple ticket creation utility backed by tickets.json."""

    def __init__(self, data_file: Path | None = None) -> None:
        self._data_file = data_file or TICKETS_FILE

    def _ensure_file(self) -> None:
        """Ensure the tickets file exists with an empty list."""
        if not self._data_file.exists():
            self._data_file.parent.mkdir(parents=True, exist_ok=True)
            with self._data_file.open("w", encoding="utf-8") as handle:
                json.dump([], handle, indent=2)

    def _load_tickets(self) -> List[Dict[str, Any]]:
        self._ensure_file()
        with self._data_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _save_tickets(self, tickets: List[Dict[str, Any]]) -> None:
        with self._data_file.open("w", encoding="utf-8") as handle:
            json.dump(tickets, handle, indent=2)

    @staticmethod
    def _next_ticket_id(tickets: List[Dict[str, Any]]) -> str:
        prefix = "T-"
        if not tickets:
            return f"{prefix}001"

        max_number = 0
        for ticket in tickets:
            ticket_id = ticket.get("ticket_id", "")
            if ticket_id.startswith(prefix):
                try:
                    max_number = max(max_number, int(ticket_id.split("-")[1]))
                except (IndexError, ValueError):
                    continue

        return f"{prefix}{max_number + 1:03d}"

    def create_ticket(self, issue_type: str, description: str, user_id: str) -> Dict[str, Any]:
        """Create a ticket and append to tickets.json."""
        tickets = self._load_tickets()
        ticket = {
            "ticket_id": self._next_ticket_id(tickets),
            "issue_type": issue_type,
            "description": description,
            "user_id": user_id,
            "status": "open",
        }
        tickets.append(ticket)
        self._save_tickets(tickets)
        return ticket

