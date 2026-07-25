import pandas as pd

class DataProcessor:
    def __init__(self, timeframe):
        self.timeframe = timeframe

    def process(self, df):
        df = df.copy()
        df = self.sort_data(df)
        df = self.remove_duplicates(df)
        df = self.fill_missing_bars(df)
        return df

    def sort_data(self, df):
        return df.sort_index()

    def remove_duplicates(self, df):
        return df[
            ~df.index.duplicated(
                keep='last'
            )
        ]

    def fill_missing_bars(self, df):
        full_range = pd.date_range(
            start=df.index.min(),
            end=df.index.max(),
            freq=self.timeframe.pandas_freq,
            tz=df.index.tz,
        )

        df = df.reindex(full_range)

        # Preserve original values
        df['close'] = df['close'].ffill()

        # Fill missing OHLC values
        for column in [
            'open',
            'high',
            'low',
        ]:
            df[column] = (
                df[column]
                .fillna(df['close'])
            )

        # No trading occurred
        for column in [
            'volume',
            'trade_count',
            'vwap',
        ]:
            df[column] = (
                df[column]
                .fillna(0)
            )

        return df
