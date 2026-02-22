from __future__ import annotations

from app.engine import FinanceEngine
from app.mcp import MCPAdapter
from app.models import FinancialEntry, InvestmentRequest, ParseResult, Profile
from app.parser import parse_financial_message


class FinanceManagerAIApp:
    """Core app façade that can be wired to API/CLI layers."""

    def __init__(self) -> None:
        self.engine = FinanceEngine()
        self.mcp = MCPAdapter()

    def health(self) -> dict:
        return {"status": "ok"}

    def parse_message(self, message: str) -> ParseResult:
        result = parse_financial_message(message)
        if result.parsed_entry:
            self.engine.add_entry(result.parsed_entry)
            self.mcp.sync_expense_log(result.parsed_entry)
        return result

    def add_entry(self, entry: FinancialEntry) -> dict:
        self.engine.add_entry(entry)
        self.mcp.sync_expense_log(entry)
        return {"status": "logged", "entry": entry.model_dump(mode="json")}

    def dashboard(self) -> dict:
        return self.engine.dashboard()

    def alerts(self) -> dict:
        return {"alerts": self.engine.generate_alerts()}

    def set_profile(self, profile: Profile) -> dict:
        stored = self.engine.set_profile(profile)
        return {"status": "saved", "profile": stored.model_dump()}

    def analyze_investment(self, request: InvestmentRequest) -> dict:
        return self.engine.analyze_investment(request).model_dump()

    def market_monitor(self) -> dict:
        market = self.mcp.pull_market_data()
        return {
            "summary": "Macro mixed, risk assets selective.",
            "macro_trends": {
                "inflation": market["inflation"],
                "interest_rates": market["rates"],
                "gdp": market["gdp_trend"],
            },
            "major_indices": market["indices"],
            "sector_rotation": market["sector_rotation"],
            "emerging_opportunities": ["quality AI infrastructure", "healthcare innovation"],
            "risk_warnings": ["valuation risk in crowded momentum trades"],
            "tldr": "Stay diversified, phase entries, preserve liquidity for volatility.",
            "actionable_insights": [
                "Review concentration >40% per asset/sector.",
                "Rebalance monthly based on target allocation.",
            ],
        }

    def execute_simulated_investment(self, confirm: bool, request: InvestmentRequest) -> dict:
        if not confirm:
            return {"status": "blocked", "reason": "Explicit confirmation required."}
        return {
            "status": "simulated_executed",
            "trade": request.model_dump(),
            "note": "No real trade executed.",
        }
