import pandas as pd

class DataProcessor:
    def __init__(self, timeframe):
        self.timeframe = timeframe

    def process(self, df):
        df = df.copy()
        self.validate(df)
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
        
        # Track where each row came from
        df['source'] = 'downloaded' 
        missing = df['close'].isna()
        df.loc[missing, 'source'] = 'filled'
 
        # Forward-fill close price
        df['close'] = df['close'].ffill() 

        # Fill OHLC from previous close
        for column in ['open', 'high', 'low']:
            if column in df.columns:
                df[column] = df[column].fillna(df['close'])

        # Fill volume-like columns with zero
        for column in ['volume', 'trade_count', 'vwap']:
            if column in df.columns:
                df[column] = df[column].fillna(0)

        return df

    def validate(self, df):
        if not df.index.is_monotonic_increasing:
            raise ValueError('Data is not sorted.')

        if df.index.duplicated().any():
            raise ValueError('Duplicate timestamps found.')

        return True
