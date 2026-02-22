from __future__ import annotations

from collections import defaultdict
from datetime import date

from app.models import AdviceResponse, EntryType, FinancialEntry, InvestmentRequest, Profile


class FinanceEngine:
    def __init__(self) -> None:
        self.entries: list[FinancialEntry] = []
        self.profile = Profile()

    def set_profile(self, profile: Profile) -> Profile:
        self.profile = profile
        return profile

    def add_entry(self, entry: FinancialEntry) -> None:
        self.entries.append(entry)

    def dashboard(self, as_of: date | None = None) -> dict:
        as_of = as_of or date.today()
        income = sum(e.amount for e in self.entries if e.entry_type == EntryType.income)
        expenses = sum(
            e.amount for e in self.entries if e.entry_type in {EntryType.expense, EntryType.bill}
        )
        investments = sum(
            e.amount for e in self.entries if e.entry_type == EntryType.investment
        )

        by_category: dict[str, float] = defaultdict(float)
        for e in self.entries:
            if e.entry_type == EntryType.expense:
                by_category[e.category] += e.amount

        monthly_expenses = max(expenses, 1)
        emergency_fund_coverage = income / monthly_expenses
        savings_rate = ((income - expenses) / income * 100) if income else 0
        net_worth = income - expenses + investments

        return {
            "as_of": as_of.isoformat(),
            "cash_flow": {"income": income, "expenses": expenses, "net": income - expenses},
            "net_worth": round(net_worth, 2),
            "asset_allocation": {"investments": investments, "cash": max(income - expenses, 0)},
            "liabilities": 0,
            "bill_due_dates": [
                {"category": e.category, "due_date": e.due_date.isoformat(), "amount": e.amount}
                for e in self.entries
                if e.entry_type == EntryType.bill and e.due_date
            ],
            "investment_performance": "requires external pricing feed",
            "savings_rate_pct": round(savings_rate, 2),
            "emergency_fund_coverage_ratio": round(emergency_fund_coverage, 2),
            "expense_breakdown": dict(by_category),
            "rule_50_30_20": self._rule_50_30_20(income, expenses),
        }

    def _rule_50_30_20(self, income: float, expenses: float) -> dict:
        if income <= 0:
            return {"status": "insufficient income data"}
        essentials_target = income * 0.5
        wants_target = income * 0.3
        savings_target = income * 0.2
        return {
            "essentials_target": round(essentials_target, 2),
            "wants_target": round(wants_target, 2),
            "savings_target": round(savings_target, 2),
            "current_spend": round(expenses, 2),
            "status": "review category tagging for precise split",
        }

    def generate_alerts(self) -> list[dict]:
        alerts: list[dict] = []
        dash = self.dashboard()
        expenses = dash["cash_flow"]["expenses"]
        income = dash["cash_flow"]["income"]
        cash = dash["asset_allocation"]["cash"]

        if dash["emergency_fund_coverage_ratio"] < 3:
            alerts.append({"type": "emergency_fund", "severity": "high", "message": "Emergency fund below 3 months."})

        if income and cash / income > 0.25:
            alerts.append({"type": "cash_drag", "severity": "medium", "message": "Idle cash exceeds 25% of income."})

        recent_expenses = [e.amount for e in self.entries if e.entry_type == EntryType.expense]
        if len(recent_expenses) >= 2:
            avg = sum(recent_expenses[:-1]) / max(len(recent_expenses[:-1]), 1)
            if avg > 0 and recent_expenses[-1] > avg * 1.3:
                alerts.append({"type": "spending_spike", "severity": "medium", "message": "Latest expense is >30% above prior average."})

        today = date.today()
        for entry in self.entries:
            if entry.entry_type == EntryType.bill and entry.due_date:
                days = (entry.due_date - today).days
                if 0 <= days <= 3:
                    alerts.append({"type": "bill_due", "severity": "high", "message": f"Bill due in {days} day(s): {entry.category}"})

        if expenses > income and income > 0:
            alerts.append({"type": "budget_overrun", "severity": "high", "message": "Expenses exceed income."})

        return alerts

    def analyze_investment(self, request: InvestmentRequest) -> AdviceResponse:
        if not self.profile.risk_tolerance:
            return AdviceResponse(
                summary="Risk profile incomplete.",
                analysis={"missing": ["risk_tolerance", "investment_horizon_years", "liquidity_needs", "geographic_preference"]},
                recommendation="Please set your profile before receiving investment guidance.",
                next_action_step="Call /profile with your preferences.",
                disclaimer="This is educational information, not guaranteed returns.",
            )

        base_risk = min(10, max(1, round(request.volatility * 2)))
        tolerance_adjust = {"low": 2, "medium": 0, "high": -1}[self.profile.risk_tolerance.value]
        risk_score = min(10, max(1, base_risk + tolerance_adjust))

        allocation = 2.0
        if self.profile.risk_tolerance.value == "high":
            allocation = 5.0
        elif self.profile.risk_tolerance.value == "medium":
            allocation = 3.0

        analysis = {
            "risk_level": self.profile.risk_tolerance.value,
            "volatility": request.volatility,
            "liquidity": request.liquidity_score,
            "sector_exposure": request.sector,
            "diversification_impact": "positive if sector underweight; negative if already concentrated",
            "time_horizon_compatibility": "strong" if (self.profile.investment_horizon_years or 0) >= 5 else "moderate",
            "pros": ["potential upside", "portfolio growth contribution"],
            "cons": ["market drawdown risk", "sector cyclicality"],
            "risk_score_1_to_10": risk_score,
            "portfolio_fit": "fits" if risk_score <= 7 else "cautious fit",
            "suggested_allocation_pct": allocation,
            "scenario_analysis": {
                "bull": "+18% expected range",
                "neutral": "+6% expected range",
                "bear": "-22% downside scenario",
            },
        }

        return AdviceResponse(
            summary=f"{request.symbol} reviewed with risk score {risk_score}/10.",
            analysis=analysis,
            recommendation=(
                "Proceed gradually using staged entries and maintain diversification."
                if risk_score <= 7
                else "Limit position size and hedge concentration risk before adding exposure."
            ),
            next_action_step="Confirm target allocation and rebalance plan.",
            disclaimer="No return is guaranteed. Diversification and risk management are essential.",
        )
