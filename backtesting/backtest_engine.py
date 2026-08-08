from backtesting.historical_data_feed import HistoricalDataFeed
from backtesting.portfolio import Portfolio
from backtesting.simulated_broker import SimulatedBroker
from backtesting.position_sizer import PositionSizer
from backtesting.trade import Trade, CompletedTrade 

class BacktestEngine:
    def __init__(
        self,
        data,
        strategy,
        symbol,
        initial_cash=10000        
    ):
        self.feed = HistoricalDataFeed(data)
        self.strategy = strategy
        self.symbol = symbol
        self.portfolio = Portfolio(initial_cash)
        self.broker = SimulatedBroker(self.portfolio)
        self.position_sizer = PositionSizer()
        self.trades = []
        self.equity_curve = []
        self.completed_trades = []
        self.open_trade = None

    def run(self):
        self.feed.reset()

        while self.feed.has_next():
            self.feed.next()            
            history = self.feed.current()

            if len(history) < self.strategy.signal.lookback:
                continue

            position = self.portfolio.get_position(self.symbol)
            signal = self.strategy.evaluate(history, position)
            latest_price = history['close'].iloc[-1]
            timestamp = history.index[-1]

            if signal == 'BUY' and position is None:
                quantity = (
                    self.position_sizer.calculate_quantity(
                        self.portfolio.cash,
                        latest_price
                    )
                )

                if quantity > 0:
                    self.broker.buy(
                        self.symbol,
                        quantity,
                        latest_price
                    )
                   
                    trade = Trade(
                        timestamp=timestamp,
                        symbol=self.symbol,
                        side='BUY',
                        quantity=quantity,
                        price=latest_price
                    )
                    
                    self.trades.append(trade)
                    self.open_trade = trade

                    print(
                        timestamp,
                        'BUY',
                        self.symbol,
                        quantity,
                        latest_price
                    )

            elif signal == 'SELL' and position is not None:
                quantity = position.quantity
                self.broker.sell(
                    self.symbol,
                    latest_price
                )
                
                trade = Trade(
                    timestamp=timestamp,
                    symbol=self.symbol,
                    side='SELL',
                    quantity=quantity,
                    price=latest_price
                )
                
                self.trades.append(trade)

                if self.open_trade is not None:
                    completed_trade = CompletedTrade(
                        entry_timestamp=self.open_trade.timestamp,
                        exit_timestamp=timestamp,
                        symbol=self.symbol,
                        quantity=self.open_trade.quantity,
                        entry_price=self.open_trade.price,
                        exit_price=latest_price
                    )

                    self.completed_trades.append(completed_trade)
                    self.open_trade = None

                print(
                    timestamp,
                    'SELL',
                    self.symbol,
                    quantity,
                    latest_price
                )
                
            portfolio_value = self.portfolio.market_value(
                {
                    self.symbol: latest_price
                }
            ) 
            
            self.equity_curve.append(
                {
                    'timestamp': timestamp,
                    'portfolio_value': portfolio_value
                }
            )
            
