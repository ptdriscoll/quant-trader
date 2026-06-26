# Quant Trader

A modular algorithmic trading framework that performs automated universe selection, signal generation, and paper-traded order execution through the Alpaca API. Strategies are implemented as independent modules and can be added without modifying the core execution engine.

## 🚀 Overview

The framework performs:

1. Market data ingestion
2. Universe selection and optimization
3. Strategy signal generation
4. Automated order execution
5. Portfolio performance tracking

The system separates responsibilities into three layers:

- **Engine Layer** (`main.py`) – Scheduling and strategy orchestration
- **Strategy Layer** (`strategies/`) – Universe selection and signal generation
- **Execution Layer** (`execution/`) – Order routing and trading friction models

## 📂 Project Structure

```text
quant-trader/
│
├── execution/
│   └── orders.py
│
├── strategies/
│   ├── base_strategy.py
│   ├── equity_sma.py
│   └── crypto_sma.py
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

| Strategy   | Universe              | Optimization | Timeframe | Buy Signal      | Sell Signal     |
| ---------- | --------------------- | ------------ | --------- | --------------- | --------------- |
| Equity SMA | Top 100 Dollar Volume | Daily        | 1m        | Price > SMA(20) | Price < SMA(20) |
| Crypto SMA | BTC, ETH              | None         | 1m        | Price > SMA(20) | Price < SMA(20) |

## 📈 Performance Tracking

Portfolio equity, cash balance, and unrealized P&L are recorded to a local SQLite database for performance analysis.

## ⚖️ License

Distributed under the MIT License.
