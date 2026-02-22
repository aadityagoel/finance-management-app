from __future__ import annotations

import re
from datetime import date, timedelta

from app.models import EntryType, FinancialEntry, ParseResult


MONEY_PATTERN = re.compile(r"(?<!\d)(\d+(?:\.\d{1,2})?)(?!\d)")


def _extract_amount(text: str) -> float | None:
    match = MONEY_PATTERN.search(text)
    return float(match.group(1)) if match else None


def parse_financial_message(message: str, today: date | None = None) -> ParseResult:
    today = today or date.today()
    text = message.strip().lower()
    amount = _extract_amount(text)

    if amount is None:
        return ParseResult(
            requires_clarification=True,
            clarification_question="I couldn't detect an amount. Please provide the value.",
        )

    recurring = "monthly" in text or "recurring" in text or "every month" in text

    if any(k in text for k in ["paid", "spent", "bought", "expense"]):
        category = "general"
        if "dinner" in text or "food" in text:
            category = "food"
        elif "rent" in text:
            category = "housing"
        return ParseResult(
            parsed_entry=FinancialEntry(
                entry_type=EntryType.expense,
                category=category,
                amount=amount,
                date=today,
                recurring=recurring,
                note=message,
            )
        )

    if any(k in text for k in ["salary", "income", "got paid", "got salary", "received"]):
        return ParseResult(
            parsed_entry=FinancialEntry(
                entry_type=EntryType.income,
                category="salary",
                amount=amount,
                date=today,
                recurring=recurring,
                note=message,
            )
        )

    if any(k in text for k in ["invested", "invest", "bought stock", "etf"]):
        symbol_match = re.search(r"(?:in|into)\s+([a-zA-Z.\-]+)", text)
        symbol = symbol_match.group(1).upper() if symbol_match else None
        if symbol is None:
            return ParseResult(
                requires_clarification=True,
                clarification_question="Which asset did you invest in?",
            )
        return ParseResult(
            parsed_entry=FinancialEntry(
                entry_type=EntryType.investment,
                category="equity",
                amount=amount,
                date=today,
                recurring=False,
                note=message,
                asset_symbol=symbol,
            )
        )

    if "bill" in text:
        due_date = today
        if "next week" in text:
            due_date = today + timedelta(days=7)
        elif "tomorrow" in text:
            due_date = today + timedelta(days=1)
        elif "in 3 days" in text:
            due_date = today + timedelta(days=3)

        category = "utilities" if "electric" in text else "bill"
        return ParseResult(
            parsed_entry=FinancialEntry(
                entry_type=EntryType.bill,
                category=category,
                amount=amount,
                date=today,
                due_date=due_date,
                recurring=recurring,
                note=message,
            )
        )

    return ParseResult(
        requires_clarification=True,
        clarification_question=(
            "I need more context. Is this an expense, income, investment, or bill?"
        ),
    )
