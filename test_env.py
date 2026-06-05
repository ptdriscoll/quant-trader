import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
import pandas as pd
import pandas_ta as ta

# 1. Load your API keys from a .env file
load_dotenv()

API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

print('\n--- Environment Check ---')

# 2. Test Alpaca connection and print out your newly updated balance
if API_KEY and SECRET_KEY:
    try:
        # Initialize the client pointing to your fresh paper account
        trading_client = TradingClient(api_key=API_KEY, secret_key=SECRET_KEY, paper=True)
        account = trading_client.get_account()
        print('Alpaca Connection: SUCCESS')
        print(f'Current Paper Portfolio Cash: ${account.cash}')
    except Exception as e:
        print(f'Alpaca Connection: FAILED. Error: {e}')
else:
    print('Alpaca Connection: FAILED. Missing keys in your .env file.')

# 3. Test that the original pandas-ta library can generate data extensions
try:
    # Create sample stock price data
    mock_data = pd.DataFrame({'close': [100, 101, 102, 103, 104, 105]})
    
    # Calculate a simple 5-day moving average using pandas-ta
    mock_data.ta.sma(length=5, append=True)
    
    print('Pandas-TA Integration: SUCCESS')
    
except Exception as e:
    print(f'Pandas-TA Integration: FAILED. Error: {e}')
