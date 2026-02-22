# Finance Manager AI

Finance Manager AI is a personal financial assistant and "AI CFO" backend service that helps users:

- Track income, expenses, bills, investments, and assets
- Maintain real-time cash flow, net worth, asset allocation, liabilities, and bill deadlines
- Parse natural-language financial messages into structured ledger entries
- Analyze portfolio risk, concentration, and diversification
- Generate proactive alerts for financial health and risk thresholds
- Integrate with external systems through MCP-compatible adapters (e.g., Grow)

## Features

- **Message parsing** for entries like:
  - `Paid 50 for dinner`
  - `Invested 2000 in Tesla`
  - `Got salary 5000`
  - `Electric bill 120 due next week`
- **Structured financial dashboard** with:
  - cash flow summary
  - net worth
  - expense breakdown
  - emergency fund coverage ratio
  - savings rate
- **Portfolio intelligence**:
  - risk score (1–10)
  - sector concentration and single-asset concentration checks
  - bull / neutral / bear scenario estimates
  - suggested allocation guidance
- **Market monitoring endpoint** with macro and index snapshot format
- **Proactive alerts**:
  - spending spikes >30%
  - emergency fund <3 months expenses
  - portfolio concentration >40%
  - high-interest debt present
  - bill due within 3 days
  - idle cash >25%
- **MCP adapter interface** for syncing logs and pulling external data safely

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open API docs at `http://127.0.0.1:8000/docs`.

## Run tests

```bash
pytest
```

## Safety notes

- This project does **not** execute real trades.
- Transaction execution must be explicitly confirmed by users.
- Investment suggestions include risk-oriented, non-guaranteed guidance.
