import pandas as pd
from pandas_ta import ema, sma
from alpaca.data.timeframe import TimeFrame
from signals.base_signal import BaseSignal

class MovingAverageCrossSignal(BaseSignal):
    timeframe = TimeFrame.Minute

    def __init__(
        self,
        fast_type='ema',
        fast_length=9,
        slow_type='sma',
        slow_length=20
    ):
        self.fast_type = fast_type.lower()
        self.fast_length = fast_length
        self.slow_type = slow_type.lower()
        self.slow_length = slow_length

    @property
    def lookback(self):
        return max(self.fast_length, self.slow_length) * 3

    def _moving_average(self, series, ma_type, length):
        if ma_type == 'ema':
            return ema(series, length=length)

        if ma_type == 'sma':
            return sma(series, length=length)

        raise ValueError(f'Unsupported moving average type: {ma_type}')

    def generate(self, df, owned, position=None):
        df = df.copy()

        df['FAST'] = self._moving_average(
            df['close'],
            self.fast_type,
            self.fast_length
        )

        df['SLOW'] = self._moving_average(
            df['close'],
            self.slow_type,
            self.slow_length
        )

        if len(df) < 2:
            return None

        previous_fast = df['FAST'].iloc[-2]
        previous_slow = df['SLOW'].iloc[-2]

        current_fast = df['FAST'].iloc[-1]
        current_slow = df['SLOW'].iloc[-1]

        if any(pd.isna(x) for x in (
            previous_fast,
            previous_slow,
            current_fast,
            current_slow
        )):
            return None

        bullish_cross = (
            previous_fast <= previous_slow and
            current_fast > current_slow
        )

        bearish_cross = (
            previous_fast >= previous_slow and
            current_fast < current_slow
        )

        if bullish_cross and not owned:
            return 'BUY'

        if bearish_cross and owned:
            return 'SELL'

        return None
