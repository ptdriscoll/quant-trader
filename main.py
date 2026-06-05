import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo # Daylight Savings Time handling for New York
from dotenv import load_dotenv

# Alpaca SDK imports
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient

# Local imports 
from strategies.equity_sma import EquitySMAStrategy
from database_manager import init_database, log_balance

# ==============================================================================
# CONFIGURATION & CLIENT INITIALIZATION
# ==============================================================================
load_dotenv()
API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

trading_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY, paper=True)
data_client = StockHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)
equity_strategy = EquitySMAStrategy(trading_client, data_client)
strategies = [equity_strategy]

init_database()
print() # Add terminal spacing

# ==============================================================================
# CONTINUOUS LOOP WITH AUTOMATED TIME-CONDITIONALS
# ==============================================================================
def main():
    print('🚀 Initializing System Engine...')
    
    # Establish dynamic, DST-safe Eastern Time timezone tracking object
    est_tz = ZoneInfo('America/New_York')
    previous_market_state = True
    for strategy in strategies:
        strategy.optimize_universe()
        print(
            f'--- {strategy.__class__.__name__} '
            f'universe size: {len(strategy.universe)} ---'
        )    
    
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
        if not previous_market_state:
            print(f'--- Market opened [{current_date}, {current_time}] ---')
            for strategy in strategies:
                strategy.optimize_universe()
                print(
                    f'--- {strategy.__class__.__name__} '
                    f'universe size: {len(strategy.universe)} ---'
                )
            previous_market_state = True    
        
        print(f'--- Starting Minute Scan [{current_date}, {current_time}] ---')    
    
        try:         
            for strategy in strategies:
                try:
                    strategy.run()
                except Exception as e:
                    print(f'🚨 Strategy Error [{strategy.__class__.__name__}]: {e}')
                
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
