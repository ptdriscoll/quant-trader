from backtesting.historical_data_feed import HistoricalDataFeed
from backtesting.portfolio import Portfolio
from backtesting.simulated_broker import SimulatedBroker

class BacktestEngine:
    def __init__(
        self,
        data,
        strategy,
        initial_cash=10000
    ):
        self.feed = HistoricalDataFeed(data)
        self.strategy = strategy
        self.portfolio = Portfolio(initial_cash)
        self.broker = SimulatedBroker(self.portfolio)

    def run(self):
        self.feed.reset()
        while self.feed.has_next():
            self.feed.next()
            
            history = self.feed.current()
            if len(history) < self.strategy.signal.lookback:
                continue

            position = self.portfolio.get_position('BTC/USD')
            signal = self.strategy.evaluate(history, position)
            latest_price = history['close'].iloc[-1]

            print(
                history.index[-1],
                signal,
                latest_price
            )
