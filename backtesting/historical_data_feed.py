import pandas as pd

class HistoricalDataFeed:
    def __init__(self, data):
        self.data = data
        self.current_index = 0

    def reset(self):
        self.current_index = 0
        
    def has_next(self):
        return self.current_index < len(self.data)        

    def next(self):
        self.current_index += 1

    def current(self):
        return self.data.iloc[:self.current_index]

    def next_bar(self):
        if not self.has_next():
            return None

        bar = self.data.iloc[self.current_index]
        timestamp = self.data.index[self.current_index]
        self.current_index += 1

        return {
            'timestamp': timestamp,
            'open': bar['open'],
            'high': bar['high'],
            'low': bar['low'],
            'close': bar['close'],
            'volume': bar['volume'],
        }
