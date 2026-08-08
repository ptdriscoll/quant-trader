class Performance:

    def __init__(
        self,
        initial_cash,
        equity_curve,
        trades
    ):
        self.initial_cash = initial_cash
        self.equity_curve = equity_curve
        self.trades = trades

    def final_value(self):
        if not self.equity_curve:
            return self.initial_cash

        return self.equity_curve[-1][
            'portfolio_value'
        ]

    def total_return(self):
        return (self.final_value() / self.initial_cash) - 1

    def total_profit(self):
        return (self.final_value() - self.initial_cash)

    def trade_count(self):
        return len(self.trades)

    def winning_trades(self):
        return 0

    def losing_trades(self):
        return 0
