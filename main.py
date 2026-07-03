import os
import time
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo # Daylight Savings Time handling for New York
from dotenv import load_dotenv

# Alpaca SDK imports
from alpaca.trading.client import TradingClient
from alpaca.data.historical import (
    StockHistoricalDataClient, 
    CryptoHistoricalDataClient
)

# Local imports 
from strategies.equity_strategy import EquityStrategy
from strategies.crypto_strategy import CryptoStrategy
from signals.price_sma_signal import PriceSMASignal
from database_manager import init_database, log_balance
from utils.api_metrics import ApiMetrics

# ==============================================================================
# CONFIGURATION & CLIENT INITIALIZATION
# ==============================================================================
load_dotenv()
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

price_signal = PriceSMASignal()
api_metrics = ApiMetrics()
init_database()

trading_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY, paper=True)
stock_data_client = StockHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)
crypto_data_client = CryptoHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)

equity_strategy = EquityStrategy(
    trading_client,
    stock_data_client,
    api_metrics,
    price_signal
)
crypto_strategy = CryptoStrategy(
    trading_client,
    crypto_data_client,
    api_metrics,
    price_signal
)
strategies = [equity_strategy, crypto_strategy]

print() # Add terminal spacing

# ==============================================================================
# CONTINUOUS LOOP WITH AUTOMATED TIME-CONDITIONALS
# ==============================================================================
def main():
    print('🚀 Initializing System Engine...')
    
    for strategy in strategies:
        strategy.optimize_universe()

    for strategy in strategies:
        strategy.run()        
    
    est_tz = ZoneInfo('America/New_York') # DST-safe Eastern Time timezone object
    api_metrics.record_request('get_clock')
    previous_market_state = trading_client.get_clock().is_open
    time.sleep(60) # Wait a minute before starting ongoing checks    
    
    # Check every 60 seconds
    while True:
        loop_start = time.time()
        try:
            api_metrics.record_request('get_clock')
            clock = trading_client.get_clock()  
            
            now_est = datetime.now(est_tz)
            current_date = now_est.strftime('%Y-%m-%d')
            current_time = now_est.strftime('%H:%M')
            
            runnable_strategies = [
                strategy
                for strategy in strategies
                if strategy.should_run(clock)
            ]
            
            # Equity market just opened        
            if clock.is_open and not previous_market_state:
                print(f'--- Equity market opened [{current_date}, {current_time}] ---')
                for strategy in strategies:
                    strategy.optimize_universe()
                previous_market_state = True           
                
            # Equity market just closed    
            elif not clock.is_open and previous_market_state:
                print(f'--- Equity market closed [{current_date}, {current_time}] ---')
                previous_market_state = False    
                    
            if not runnable_strategies:
                print(f'--- No runnable strategies. Sleeping... ---')
                
                if clock.next_open:
                    seconds_until_open = (clock.next_open - now_est).total_seconds() 
                else:
                    seconds_until_open = 300            
                
                sleep_time = max(60, min(seconds_until_open, 1800)) # Wait at least 1 minute, no more than 30
                time.sleep(sleep_time)
                continue 
            
            print(f'--- Starting Minute Scan [{current_date}, {current_time}] ---')         

            for strategy in runnable_strategies:
                print(f'Running {strategy.NAME}')
                strategy.run()
                
            elapsed = time.time() - loop_start # For locking exact 60-second boundaries            
            print(f'--- Scan Finished. Local Math Engine Execution Time: {elapsed:.2f}s ---')
            
            # Fetch, display, and record financial progress entries
            api_metrics.record_request('get_account')
            account = trading_client.get_account()
            api_metrics.record_request('get_all_positions')
            positions = trading_client.get_all_positions()
            total_unrealized_pl = sum(float(position.unrealized_pl) for position in positions)
            log_balance(
                equity=float(account.portfolio_value),
                cash=float(account.cash),
                pl=total_unrealized_pl
            )
            api_metrics.print_summary()
            
            sleep_duration = max(0, 60 - elapsed)
            time.sleep(sleep_duration)
            
        except Exception as e:
            api_metrics.record_failure()
            print(f"🚨 Global Engine Error [{type(e).__name__}]: {e}")
            traceback.print_exc()
            time.sleep(10)            

if __name__ == '__main__':
    main()
