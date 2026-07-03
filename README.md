# Quant Trader

A modular algorithmic trading framework that performs automated universe selection, signal generation, and paper-traded order execution through the Alpaca API. Strategies are implemented as independent modules and can be added without modifying the core execution engine.

## 🚀 Overview

The framework performs:

1. Market data ingestion
2. Universe selection and optimization
3. Strategy signal generation
4. Automated order execution
5. Portfolio performance tracking

The system separates responsibilities:

- **Engine Layer** (`main.py`) – Scheduling and strategy orchestration
- **Strategy Layer** (`strategies/`) – Universe selection and coordinating signals and risks 
- **Signal Layer** (`signals/`) – Buy and sell signal generation
- **Risk Layer** (`risk/`) – Position exit and trade risk management
- **Execution Layer** (`execution/`) – Order routing and trading friction models

## 📂 Project Structure

```text
quant-trader/
│
├── execution/
│   └── orders.py
│
├── risk/
│   ├── base_risk.py
│   └── fixed_stop_loss_risk.py
│
├── signals/
│   ├── base_signal.py
│   ├── moving_average_cross_signal.py
│   └── price_sma_signal.py
│
├── strategies/
│   ├── base_strategy.py
│   ├── equity_strategy.py
│   └── crypto_strategy.py
│
├── utils/
│   └── api_metrics.py
│
├── database_manager.py
├── main.py
└── trading_history.db
```

## 🛠️ Installation and Workspace Setup

This project supports isolated workflows using either **Conda** or native **Pip**.

### Option A: Conda Installation (Recommended)

This method utilizes `conda-forge` to manage all analytical frameworks and API wrapper libraries inside an isolated environment.

```bash
# 1. Create the environment with a stable Python baseline
conda create -n quant_trading python=3.12 -y

# 2. Activate the workspace
conda activate quant_trading

# 3. Install developer SDK wrappers and utility dependencies via conda-forge
conda install -c conda-forge alpaca-py pandas-ta python-dotenv tzdata  pytz -y

# 4. If using use Miniconda instead of the full Anaconda distribution, install pandas
conda install pandas -y
```

### Option B: Standard Python Installation (Pip)

For setups running outside a Conda management environment, use native Python virtualization and the Python Package Index (PyPI).

```bash
# 1. Create a native virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3. Upgrade your package installer tool
pip install --upgrade pip

# 4. Install the full pipeline package bundle
pip install pandas alpaca-py pandas-ta python-dotenv tzdata  pytz
```

To set up Alpaca Paper Trading, create an account at [https://alpaca.markets](https://alpaca.markets) and get an API key and secret. Then rename the `.env.example` file to `.env` and set the variables `ALPACA_PAPER_KEY` and `ALPACA_PAPER_SECRET` to match those from your account.

## 🚦 Strategies

| Strategy | Universe | Optimization |
|----------|----------|--------------|
| Equity | Top 100 U.S. stocks by daily dollar volume | Daily |
| Crypto | Top-volume cryptocurrency pairs (currently BTC/USD, ETH/USD) | Static |

## 📈 Signals

| Signal | Timeframe | Buy Signal | Sell Signal |
|--------|-----------|------------|-------------|
| Price SMA | 1 minute | Price > SMA(20) | Price < SMA(20) |
| Moving Average Cross | 1 minute | EMA crosses above SMA | EMA crosses below SMA |

## 🛡 Risk Management

| Risk Model | Description |
|------------|-------------|
| None | No risk management beyond signal reversal |
| Fixed Stop Loss | Exit after fixed percentage loss |

## 📊 Performance Tracking

Portfolio equity, cash balance, and unrealized P&L are recorded to a local SQLite database for performance analysis.

## 📡 API Monitoring

The framework tracks Alpaca API usage in real time, including:

- Total requests
- Requests per minute
- Peak requests per minute
- Failed requests
- Retry attempts
- Requests grouped by endpoint

These metrics help monitor rate limits and diagnose connectivity issues during long-running sessions.

## ⚖️ License

Distributed under the MIT License.
