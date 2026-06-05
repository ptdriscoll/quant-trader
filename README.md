# Quant Trader

A modular, automated quantitative trading framework that performs global market data ingestion, algorithmic asset filtering, and multi-ticker execution loops using the Alpaca Paper Trading API.

## 🚀 System Architecture

The application implements a high-utility 5-stage quantitative pipeline split across modular files to isolate strategic logic from data logging and state preservation:

1. **Bulk Ingestion**: Downloads thousands of active US equities from the exchange dynamically.
2. **Price Filter Safety**: Screens out highly volatile penny stocks and un-diversifiable high-priced assets.
3. **Math Ranking Engine**: Sorts the filtered market by Daily Dollar Volume via lightweight snapshots to extract an elite 100-ticker subset.
4. **The 60s Execution Loop**: Performs fast, in-memory `pandas` math scans across the top 100 stocks every 60 seconds using minute-by-minute historical bars.
5. **Friction Model**: Artificially penalizes buy/sell fills to accurately simulate bid-ask spreads, slippage, and SEC/FINRA regulatory trading fees.

## 📂 Project Structure

```text
quant-trader/
│
├── .env                    # Secret API credentials (ignored by git)
├── .env.example            # Configuration template for developers
├── .gitignore              # Prevents tracking of environment and database files
├── trading_history.db      # Local SQLite database tracking equity growth
│
├── database_manager.py     # State logger and database management functions
└── main.py                 # Core market scanning loop and strategic execution
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

* **Automated Daily Trigger**: Every morning at 09:00 AM, the bot triggers a time-conditional hook that rebuilds and ranks the top 100 liquidity list completely hands-free.
* **Buy Conditions (Entry)**: Triggers an order if an asset belongs to the optimized top 100 list, its current minute close crosses above its 20-period Simple Moving Average (SMA), and the portfolio does not already contain it.
* **Sell Conditions (Exit)**: Triggers an order if an owned asset's close price falls below its 20-period SMA, signaling a technical trend reversal.

## 📈 Performance Tracking

The bot query-tracks accounting metrics from Alpaca's clearing engine on every loop cycle. Financial data points are stored in a local SQLite database table (`portfolio_history`) to chart equity curve growth and measure the algorithm's mathematical profit factors over time.

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.
