import sys
import time
import pandas as pd
from pandas_ta import sma
from execution.orders import execute_order

from alpaca.trading.enums import OrderSide, AssetClass, AssetStatus
from alpaca.trading.requests import GetAssetsRequest

from alpaca.data.requests import StockBarsRequest, StockSnapshotRequest
from alpaca.data.timeframe import TimeFrame

class EquitySMAStrategy:
    def __init__(self, trading_client, data_client):
        self.trading_client = trading_client
        self.data_client = data_client
        self.universe = []
        self.execute_order = execute_order

    def optimize_universe(self):
        """Checks all 8,000+ tickers using light snapshots and gets top 100."""
        print('⏰ Running comprehensive market optimization across all stocks...')
        
        try:
            # Step 1: Bulk ingestion (get all 8,000+ active symbols)
            search_params = GetAssetsRequest(status=AssetStatus.ACTIVE, asset_class=AssetClass.US_EQUITY)
            all_assets = self.trading_client.get_all_assets(search_params)
            all_symbols = [a.symbol for a in all_assets if a.tradable and a.marginable]
            
            processed_candidates = []
            chunk_size = 250
            
            # Sift through market using lightweight, API-safe chunks
            for i in range(0, len(all_symbols), chunk_size):
                symbol_chunk = all_symbols[i:i + chunk_size]
                snapshot_request = StockSnapshotRequest(symbol_or_symbols=symbol_chunk)
                snapshots = self.data_client.get_stock_snapshot(snapshot_request)
                
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
            self.universe = top_100_df['ticker'].tolist()
            
            print(f'✅ Global optimization complete. Tracking the top {len(self.universe)} stocks.')
            
        except Exception as e:
            print(f'❌ Comprehensive optimization failed: {e}.')
            sys.exit(1) 
        
    def generate_signal(self, close, sma, owned):
        if close > sma and not owned:
            return 'BUY'

        if close < sma and owned:
            return 'SELL'

        return None

    def run(self):
        if not self.universe:
            print('⚠️ Universe is empty. Run optimize_universe() first.')
            return

        try:
            # 1. Fetch latest market data for universe
            request = StockBarsRequest(
                symbol_or_symbols=self.universe,
                timeframe=TimeFrame.Minute,
                limit=30
            )

            bars = self.data_client.get_stock_bars(request)
            master_df = bars.df

            # 2. Get current positions
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
                            'equity',
                            ticker,
                            OrderSide.BUY,
                            latest_close
                        )

                    elif signal == 'SELL':
                        self.execute_order(
                            self.trading_client,
                            'equity',
                            ticker,
                            OrderSide.SELL,
                            latest_close
                        )

                except KeyError:
                    # No data for ticker
                    continue

        except Exception as e:
            print(f'❌ Strategy run failed: {e}')         
