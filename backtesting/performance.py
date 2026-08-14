class Performance:

    def __init__(
        self,
        initial_cash,
        equity_curve,
        trades,
        completed_trades
    ):
        self.initial_cash = initial_cash
        self.equity_curve = equity_curve
        self.trades = trades
        self.completed_trades = completed_trades

    def final_value(self):
        if not self.equity_curve:
            return self.initial_cash
            
        return self.equity_curve[-1]['portfolio_value']

    def total_return(self):
        return (self.final_value() / self.initial_cash) - 1

    def total_profit(self):
        return (self.final_value() - self.initial_cash)

    def trade_count(self):
        return len(self.trades)

    def completed_trade_count(self):
        return len(self.completed_trades)

    def winning_trades(self):
        return [
            trade
            for trade in self.completed_trades
            if trade.profit > 0
        ]

    def losing_trades(self):
        return [
            trade
            for trade in self.completed_trades
            if trade.profit < 0
        ]

    def win_rate(self):
        if not self.completed_trades:
            return 0

        return (
            len(self.winning_trades())
            / len(self.completed_trades)
        )

    def average_win(self):
        winners = self.winning_trades()

        if not winners:
            return 0

        return sum(
            trade.profit
            for trade in winners
        ) / len(winners)

    def average_loss(self):
        losers = self.losing_trades()

        if not losers:
            return 0

        return sum(
            trade.profit
            for trade in losers
        ) / len(losers)

    def profit_factor(self):
        winners = self.winning_trades()
        losers = self.losing_trades()

        gross_profit = sum(
            trade.profit
            for trade in winners
        )

        gross_loss = abs(
            sum(
                trade.profit
                for trade in losers
            )
        )

        if gross_loss == 0:
            return float('inf')

        return gross_profit / gross_loss
