from datetime import date

from app.models import EntryType
from app.parser import parse_financial_message


def test_parse_expense_message() -> None:
    result = parse_financial_message("Paid 50 for dinner", today=date(2026, 1, 10))
    assert result.parsed_entry is not None
    assert result.parsed_entry.entry_type == EntryType.expense
    assert result.parsed_entry.amount == 50


def test_parse_investment_message() -> None:
    result = parse_financial_message("Invested 2000 in Tesla", today=date(2026, 1, 10))
    assert result.parsed_entry is not None
    assert result.parsed_entry.entry_type == EntryType.investment
    assert result.parsed_entry.asset_symbol == "TESLA"


def test_parse_bill_message_due_next_week() -> None:
    result = parse_financial_message("Electric bill 120 due next week", today=date(2026, 1, 10))
    assert result.parsed_entry is not None
    assert result.parsed_entry.entry_type == EntryType.bill
    assert result.parsed_entry.due_date == date(2026, 1, 17)
