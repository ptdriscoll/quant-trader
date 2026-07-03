import pandas as pd
from pandas_ta import sma
from alpaca.data.timeframe import TimeFrame
from signals.base_signal import BaseSignal

class PriceSMASignal(BaseSignal):
    timeframe = TimeFrame.Minute

    def __init__(self, length=20):
        self.length = length

    @property
    def lookback(self):
        return self.length * 3

    def generate(self, df, owned, position=None):
        df = df.copy()

        df['SMA'] = sma(
            df['close'],
            length=self.length
        )

        latest_close = df['close'].iloc[-1]
        latest_sma = df['SMA'].iloc[-1]

        if pd.isna(latest_sma):
            return None

        if latest_close > latest_sma and not owned:
            return 'BUY'

        if latest_close < latest_sma and owned:
            return 'SELL'

        return None
