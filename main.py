import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo # Daylight Savings Time handling for New York
import pandas as pd
import pandas_ta as ta
from dotenv import load_dotenv

# Alpaca SDK imports
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce, AssetClass, AssetStatus
from alpaca.trading.requests import MarketOrderRequest, GetAssetsRequest

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockSnapshotRequest
from alpaca.data.timeframe import TimeFrame

# Local logging 
from database_manager import init_database, log_balance

# ==============================================================================
# 1. CONFIGURATION & CLIENT INITIALIZATION
# ==============================================================================
load_dotenv()
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

# Friction adjustments (Friction Model)
SLIPPAGE_PCT = 0.0002       # Simulates a 0.02% bid-ask spread penalty
REG_FEE_PER_SELL = 0.00002  # Simulates fractional SEC/FINRA selling fees

trading_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY, paper=True)
data_client = StockHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)

optimized_tickers = []
init_database()
print() # Add terminal spacing

# ==============================================================================
# 2. THE ONCE-A-DAY FILTER & RANK PIPELINE (Steps 1, 2, & 3)
# ==============================================================================
def run_daily_ticker_optimization():
    """Checks all 8,000+ tickers using light snapshots and gets top 100."""
    global optimized_tickers
    print('⏰ Running comprehensive market optimization across all stocks...')
    
    try:
        # Step 1: Bulk ingestion (get all 8,000+ active symbols)
        search_params = GetAssetsRequest(status=AssetStatus.ACTIVE, asset_class=AssetClass.US_EQUITY)
        all_assets = trading_client.get_all_assets(search_params)
        all_symbols = [a.symbol for a in all_assets if a.tradable and a.marginable]
        
        processed_candidates = []
        chunk_size = 250
        
        # Sift through market using lightweight, API-safe chunks
        for i in range(0, len(all_symbols), chunk_size):
            symbol_chunk = all_symbols[i:i + chunk_size]
            snapshot_request = StockSnapshotRequest(symbol_or_symbols=symbol_chunk)
            snapshots = data_client.get_stock_snapshot(snapshot_request)
            
            for ticker, snapshot in snapshots.items():
                if snapshot is None or snapshot.daily_bar is None:
                    continue
                    
                latest_close = snapshot.daily_bar.close
                latest_volume = snapshot.daily_bar.volume
                dollar_volume = latest_close * latest_volume
                
                # Step 2: Apply price-safety filter across entire stock market
                if 15 <= latest_close <= 200:
                    processed_candidates.append({
                        'ticker': ticker,
                        'dollar_volume': dollar_volume
                    })
            time.sleep(0.1)

        ranking_df = pd.DataFrame(processed_candidates)
        
        # Step 3: Sort entire U.S. market and extract mathematical top 100 liquidity targets
        top_100_df = ranking_df.sort_values(by='dollar_volume', ascending=False).head(100)
        optimized_tickers = top_100_df['ticker'].tolist()
        
        print(f'✅ Global optimization complete. Tracking the top {len(optimized_tickers)} stocks.')
        
    except Exception as e:
        print(f'❌ Comprehensive optimization failed: {e}.')
        sys.exit(1) 

# ==============================================================================
# 3. STRATEGY CORE & FRICTION MODELING (Steps 4 & 5)
# ==============================================================================
def execute_quant_order(ticker, side_direction, current_market_price):
    """Submits order while logging the true cost, including real-world friction penalties."""
    try:
        # Step 5: Friction Model calculations
        if side_direction == OrderSide.BUY:
            # Realistically pays slightly more than the displayed ticker price due to the spread
            simulated_execution_price = current_market_price * (1 + SLIPPAGE_PCT)
            print(f' Buying {ticker} | Display: ${current_market_price:.2f} | Simulated Fill: ${simulated_execution_price:.2f}')
        else:
            # Receives slightly less when selling, and must pay regulatory micro-fees
            simulated_execution_price = (current_market_price * (1 - SLIPPAGE_PCT)) - REG_FEE_PER_SELL
            print(f' Selling {ticker} | Display: ${current_market_price:.2f} | Simulated Fill: ${simulated_execution_price:.2f}')
            
        order_data = MarketOrderRequest(
            symbol=ticker,
            qty=1,
            side=side_direction,
            time_in_force=TimeInForce.DAY
        )
        trading_client.submit_order(order_data=order_data)
        print(f'    ✅ Order dispatched safely for {ticker}.')
        
    except Exception as e:
        print(f'    ❌ Execution failed for {ticker}: {e}')
        
# ==============================================================================
# 4. CONTINUOUS LOOP WITH AUTOMATED TIME-CONDITIONALS
# ==============================================================================
def main():
    print('🚀 Initializing System Engine...')
    
    # Establish dynamic, DST-safe Eastern Time timezone tracking object
    est_tz = ZoneInfo('America/New_York')
    
    run_daily_ticker_optimization()
    previous_market_state = True 
    
    while True:
        clock = trading_client.get_clock()        
        loop_start = time.time()
        now_est = datetime.now(est_tz)
        current_date = now_est.strftime('%Y-%m-%d')
        current_time = now_est.strftime('%H:%M')
            
        # Market closed    
        if not clock.is_open:
            if previous_market_state: # Previous state was open
                print(f'--- Market closed [{current_date}, {current_time}]. Sleeping... ---')
                previous_market_state = False
            if clock.next_open:
                seconds_until_open = (clock.next_open - now_est).total_seconds() 
            else:
                seconds_until_open = 300            
            sleep_time = max(60, min(seconds_until_open, 1800)) # Wait at least 1 minute, no more than 30
            time.sleep(sleep_time)
            continue
        
        # Market just opened    
        if not previous_market_state: # Previous state was closed
            print(f'--- Market opened [{current_date}, {current_time}] ---')
            run_daily_ticker_optimization() 
            previous_market_state = True 
        
        print(f'--- Starting Minute Scan [{current_date}, {current_time}] ---')    
    
        try:            
            # Step 4: Fast in-memory batch request for the 100 optimized tickers
            request_params = StockBarsRequest(
                symbol_or_symbols=optimized_tickers,
                timeframe=TimeFrame.Minute,
                limit=30
            )
            bars = data_client.get_stock_bars(request_params)
            master_df = bars.df
            current_positions = [p.symbol for p in trading_client.get_all_positions()]
            
            for ticker in optimized_tickers:
                try:
                    ticker_df = master_df.loc[ticker]                    
                    ticker_df['SMA_20'] = ta.sma(ticker_df['close'], length=20) # Core math indicator layer
                    latest_close = ticker_df['close'].iloc[-1]
                    latest_sma = ticker_df['SMA_20'].iloc[-1]
                    is_owned = ticker in current_positions
                    
                    if latest_close > latest_sma and not is_owned:
                        execute_quant_order(ticker, OrderSide.BUY, latest_close)
                    elif latest_close < latest_sma and is_owned:
                        execute_quant_order(ticker, OrderSide.SELL, latest_close)
                        
                except KeyError: 
                    continue # Skips stocks lacking concrete transaction volume
            
            elapsed = time.time() - loop_start # For locking exact 60-second boundaries            
            print(f'--- Scan Finished. Local Math Engine Execution Time: {elapsed:.2f}s ---')
            
            # Fetch, display, and record financial progress entries
            account = trading_client.get_account()
            positions = trading_client.get_all_positions()
            total_unrealized_pl = sum(float(position.unrealized_pl) for position in positions)
            log_balance(
                equity=float(account.portfolio_value),
                cash=float(account.cash),
                pl=total_unrealized_pl
            )
            
            sleep_duration = max(0, 60 - elapsed)
            time.sleep(sleep_duration)
            
        except Exception as e:
            print(f'🚨 Global Engine Error: {e}')
            time.sleep(10)

if __name__ == '__main__':
    main()
