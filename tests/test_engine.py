from datetime import date, timedelta

from app.engine import FinanceEngine
from app.models import EntryType, FinancialEntry, InvestmentRequest, Profile, RiskTolerance


def test_dashboard_and_alerts() -> None:
    engine = FinanceEngine()
    engine.add_entry(FinancialEntry(entry_type=EntryType.income, category="salary", amount=5000, date=date.today()))
    engine.add_entry(FinancialEntry(entry_type=EntryType.expense, category="food", amount=100, date=date.today()))
    engine.add_entry(FinancialEntry(entry_type=EntryType.expense, category="food", amount=200, date=date.today()))
    engine.add_entry(
        FinancialEntry(
            entry_type=EntryType.bill,
            category="utilities",
            amount=120,
            date=date.today(),
            due_date=date.today() + timedelta(days=2),
        )
    )

    dash = engine.dashboard()
    assert dash["cash_flow"]["income"] == 5000
    assert dash["cash_flow"]["expenses"] == 420

    alerts = engine.generate_alerts()
    assert any(a["type"] == "bill_due" for a in alerts)


def test_analyze_investment_requires_profile_then_returns_analysis() -> None:
    engine = FinanceEngine()
    req = InvestmentRequest(symbol="NVDA", amount=500, sector="technology", volatility=4, liquidity_score=8)

    missing = engine.analyze_investment(req)
    assert "Risk profile incomplete" in missing.summary

    engine.set_profile(
        Profile(
            risk_tolerance=RiskTolerance.medium,
            investment_horizon_years=8,
            liquidity_needs="medium",
            geographic_preference="US",
        )
    )
    advice = engine.analyze_investment(req)
    assert advice.analysis["risk_score_1_to_10"] >= 1
    assert advice.analysis["suggested_allocation_pct"] == 3.0
