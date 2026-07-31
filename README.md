# Helix

Helix is an experimental market analysis engine built with Python and MetaTrader 5.

Instead of trying to predict the future, Helix focuses on understanding the current market context through transparent and explainable rules.

> Helix does not try to predict the future. It seeks to understand the present.

## Current capabilities

- MetaTrader 5 integration
- M5 candle data retrieval
- EMA20 and EMA50 trend analysis
- RSI confirmation
- Trend confidence scoring
- Market state classification
- Explainable market analysis
- Automated tests

## Analysis pipeline

```text
MetaTrader 5
      ↓
Market Data
      ↓
Indicators
      ↓
Trend Direction
      ↓
Confidence Score
      ↓
Market State
      ↓
Explanation
Market states

Helix currently classifies the market into five possible states:

strong_uptrend
weak_uptrend
neutral
weak_downtrend
strong_downtrend
Project structure
helix/
├── src/
│   ├── analysis/
│   │   ├── confidence.py
│   │   ├── engine.py
│   │   ├── explanation.py
│   │   ├── state.py
│   │   └── trend.py
│   └── market_data.py
├── tests/
├── research/
├── run_helix.py
├── CHANGELOG.md
├── HELIX_PRINCIPLES.md
└── README.md
Requirements
Python
MetaTrader 5 desktop terminal
An authenticated MT5 account
MetaTrader5 Python package
pandas
pytest

Install the dependencies:

python -m pip install MetaTrader5 pandas pytest
Running Helix

Keep MetaTrader 5 open and authenticated.

Configure the symbol inside run_helix.py:

SYMBOL = "WINQ26"

Then run:

python run_helix.py

Example output:

================ HELIX LIVE ANALYSIS ================

Asset: WINQ26
Timeframe: M5
Direction: DOWN
Confidence: 89.06%
State: strong_downtrend

Helix also generates a textual explanation describing the main factors behind the classification.

Running the tests
python -m pytest -v

Current test coverage includes:

Uptrend detection
Downtrend detection
Sideways detection
Confidence calculation
Market state classification
Explanation warnings
Input validation
Project status
Sprint 1
Initial market data structure
EMA and RSI studies
First trend analysis modules
Sprint 2
Trend analysis
Confidence engine
Market state classification
Unified analysis engine
MetaTrader 5 integration
Explanation layer
Automated tests

Sprint 2 is complete.

Principles

The complete project principles are documented in:

HELIX_PRINCIPLES.md
Research

Research notes, indicator observations and behavioral comparisons are stored in:

research/
Disclaimer

Helix is an experimental and educational project.

It does not provide financial advice and does not guarantee market results. The current version analyzes market context and does not execute trades.

License

License not yet defined.
