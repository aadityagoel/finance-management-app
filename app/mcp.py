from __future__ import annotations

from typing import Any

from app.models import FinancialEntry


class MCPAdapter:
    """Simple MCP-compatible adapter abstraction.

    This implementation is intentionally in-memory and non-transactional.
    Replace methods with real MCP server calls in production.
    """

    def __init__(self) -> None:
        self._synced_entries: list[dict[str, Any]] = []

    def sync_expense_log(self, entry: FinancialEntry) -> dict[str, Any]:
        payload = entry.model_dump(mode="json")
        self._synced_entries.append(payload)
        return {"status": "synced", "entry": payload}

    def fetch_portfolio_data(self) -> dict[str, Any]:
        return {
            "provider": "mock-grow",
            "positions": [
                {"symbol": "AAPL", "value": 3200, "sector": "technology"},
                {"symbol": "XLV", "value": 1400, "sector": "healthcare"},
            ],
        }

    def pull_market_data(self) -> dict[str, Any]:
        return {
            "inflation": "moderating",
            "rates": "stable",
            "gdp_trend": "resilient",
            "indices": {
                "SP500": "+0.6%",
                "NASDAQ": "+0.9%",
                "DOW": "+0.2%",
            },
            "sector_rotation": "quality growth with selective defensives",
        }
