import pandas as pd
from pandas_ta import sma
from execution.orders import execute_order
from strategies.base_strategy import BaseStrategy

from alpaca.trading.enums import OrderSide
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

class CryptoSMAStrategy(BaseStrategy):
    NAME = 'CryptoSMAStrategy'
    ASSET_TYPE = 'crypto'
    TOP_VOLUME_CRYPTO = [
        'BTC/USD',
        'ETH/USD',
        'SOL/USD',
        'AVAX/USD',
        'DOGE/USD',
        'LINK/USD'    
    ]
    
    def __init__(self, trading_client, data_client, api_metrics):
        self.trading_client = trading_client
        self.data_client = data_client
        self.api_metrics = api_metrics
        self.universe = []
        self.execute_order = execute_order
        
    def should_run(self, clock):
        return True        
        
    def optimize_universe(self):
        self.universe = self.TOP_VOLUME_CRYPTO[0:2]
        print(
            f'✅ [{self.NAME}] '
            f'Tracking {len(self.universe)} crypto pairs.'
        )
    
    def generate_signal(self, close, sma, owned):
        if close > sma and not owned:
            return 'BUY'

        if close < sma and owned:
            return 'SELL'

        return None      
        
    def run(self):
        if not self.universe:
            raise RuntimeError(
                f'[{self.NAME}] Universe is empty. Run optimize_universe() first.'
            )

        try:
            # 1. Fetch latest market data for universe
            request = CryptoBarsRequest(
                symbol_or_symbols=self.universe,
                timeframe=TimeFrame.Minute,
                limit=30
            )
            
            self.api_metrics.record_request('get_crypto_bars')
            bars = self.data_client.get_crypto_bars(request)
            master_df = bars.df 
            if master_df.empty:
                print(f'⚠️ [{self.NAME}] No market data returned.')
                return            
    
            # 2. Get current positions
            self.api_metrics.record_request('get_all_positions')
            positions = self.trading_client.get_all_positions()        
            current_positions = {p.symbol for p in positions}
            
            # 3. Loop universe
            for ticker in self.universe:
                try:
                    df = master_df.loc[ticker].copy()
                    df['SMA_20'] = sma(df['close'], length=20)

                    latest_close = df['close'].iloc[-1]
                    latest_sma = df['SMA_20'].iloc[-1]
                    is_owned = ticker in current_positions
                    
                    if pd.isna(latest_sma):
                        continue

                    # 4. Generate signal
                    signal = self.generate_signal(
                        latest_close,
                        latest_sma,
                        is_owned
                    )

                    # 5. Execute
                    if signal == 'BUY':
                        self.execute_order(
                            self.trading_client,
                            self.api_metrics,
                            self.ASSET_TYPE,
                            ticker,
                            OrderSide.BUY,
                            latest_close
                        )

                    elif signal == 'SELL':
                        self.execute_order(
                            self.trading_client,
                            self.api_metrics,
                            self.ASSET_TYPE,
                            ticker,
                            OrderSide.SELL,
                            latest_close
                        )

                except KeyError:
                    # No data for ticker
                    continue 
                
        except Exception as e:
            print(f'❌ [{self.NAME}] Strategy run failed: {e}')    
