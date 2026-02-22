from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from enum import Enum
from typing import Literal


class EntryType(str, Enum):
    expense = "expense"
    income = "income"
    investment = "investment"
    bill = "bill"
    asset = "asset"
    liability = "liability"


class RiskTolerance(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass
class FinancialEntry:
    entry_type: EntryType
    category: str
    amount: float
    date: date
    recurring: bool = False
    note: str | None = None
    due_date: date | None = None
    asset_symbol: str | None = None
    sector: str | None = None

    def model_dump(self, mode: str | None = None) -> dict:
        data = asdict(self)
        if mode == "json":
            if self.date:
                data["date"] = self.date.isoformat()
            if self.due_date:
                data["due_date"] = self.due_date.isoformat()
            data["entry_type"] = self.entry_type.value
        return data


@dataclass
class ParseResult:
    requires_clarification: bool = False
    clarification_question: str | None = None
    parsed_entry: FinancialEntry | None = None


@dataclass
class Profile:
    risk_tolerance: RiskTolerance | None = None
    investment_horizon_years: int | None = None
    liquidity_needs: Literal["low", "medium", "high"] | None = None
    geographic_preference: str | None = None
    mode: Literal["balanced", "aggressive_growth", "capital_preservation"] = "balanced"

    def model_dump(self, mode: str | None = None) -> dict:
        data = asdict(self)
        if self.risk_tolerance:
            data["risk_tolerance"] = self.risk_tolerance.value
        return data


@dataclass
class InvestmentRequest:
    symbol: str
    amount: float
    sector: str
    volatility: float
    liquidity_score: float

    def model_dump(self, mode: str | None = None) -> dict:
        return asdict(self)


@dataclass
class AdviceResponse:
    summary: str
    analysis: dict
    recommendation: str
    next_action_step: str
    disclaimer: str

    def model_dump(self, mode: str | None = None) -> dict:
        return asdict(self)
