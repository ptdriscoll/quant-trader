# Quant Trader

A modular quantitative trading framework that separates market orchestration, strategy logic, and execution layers while performing automated universe selection, signal generation, and paper-traded order execution through the Alpaca API.

## 🚀 System Architecture

The application implements a five-stage quantitative pipeline split across modular components to separate market orchestration, strategy logic, execution, and performance tracking:

1. **Bulk Ingestion**: Downloads thousands of active US equities from the exchange dynamically.
2. **Price Filter Safety**: Screens out highly volatile penny stocks and un-diversifiable high-priced assets.
3. **Math Ranking Engine**: Sorts the filtered market by Daily Dollar Volume via lightweight snapshots to extract an elite 100-ticker subset.
4. **Strategy Engine**: Executes modular trading strategies against the optimized universe using minute-level market data.
5. **Execution Layer**: Centralizes order routing, time-in-force selection, and friction modeling to simulate real-world trading costs.

The system separates responsibilities into three layers:

- **Engine Layer** (`main.py`) – Handles scheduling, market hours, and strategy orchestration.
- **Strategy Layer** (`strategies/`) – Generates trading signals and manages universe selection.
- **Execution Layer** (`execution/`) – Routes orders and applies realistic trading friction models.

## 📂 Project Structure

```text
quant-trader/
│
├── .env
├── .env.example
├── .gitignore
├── trading_history.db
│
├── main.py               # Engine coordinator and market-hours scheduler
├── database_manager.py   # SQLite logging and portfolio history
│
├── strategies/
│   ├── base_strategy.py  # Shared strategy interface
│   ├── crypto_sma.py     # Crypto-based strategy
│   └── equity_sma.py     # SMA-based equity strategy
│
└── execution/
    └── orders.py         # Centralized order execution and friction modeling
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

## 🚦 Strategic Execution Rules

* **Automated Daily Optimization**: Rebuilds and re-ranks the liquidity universe whenever the market opens, ensuring the strategy operates on current market conditions.
* **Buy Conditions (Entry)**: Triggers an order when an asset belongs to the optimized top-100 universe, its current price is above its 20-period SMA, and the portfolio does not already contain it.
* **Sell Conditions (Exit)**: Triggers an order when an owned asset's price falls below its 20-period SMA.

## 📈 Performance Tracking

The bot records portfolio metrics from Alpaca on each execution cycle. Financial data points are stored in a local SQLite database table (`portfolio_history`) to chart equity curve growth and measure the algorithm's mathematical profit factors over time.

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.
