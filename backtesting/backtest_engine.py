from backtesting.historical_data_feed import HistoricalDataFeed

class BacktestEngine:
    def __init__(self, data, strategy):
        self.feed = HistoricalDataFeed(data)
        self.strategy = strategy

    def run(self):
        self.feed.reset()
        
        while self.feed.has_next():
            self.feed.next()
            history = self.feed.current()
            
            if len(history) < self.strategy.signal.lookback:
                continue

            signal = self.strategy.evaluate(history)
            print(history.index[-1], signal)
