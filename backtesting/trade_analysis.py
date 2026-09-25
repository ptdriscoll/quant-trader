from statistics import mean, median

class TradeAnalysis:
    def __init__(self, completed_trades):
        self.completed_trades = completed_trades

    def trade_count(self):
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

    def average_profit(self):
        if not self.completed_trades:
            return 0

        return mean(
            trade.profit
            for trade in self.completed_trades
        )

    def median_profit(self):
        if not self.completed_trades:
            return 0

        return median(
            trade.profit
            for trade in self.completed_trades
        )

    def average_win(self):
        winners = self.winning_trades()

        if not winners:
            return 0

        return mean(
            trade.profit
            for trade in winners
        )

    def average_loss(self):
        losers = self.losing_trades()

        if not losers:
            return 0

        return mean(
            trade.profit
            for trade in losers
        )

    def largest_win(self):
        winners = self.winning_trades()

        if not winners:
            return 0

        return max(
            trade.profit
            for trade in winners
        )

    def largest_loss(self):
        losers = self.losing_trades()

        if not losers:
            return 0

        return min(
            trade.profit
            for trade in losers
        )

    def gross_profit(self):
        return sum(
            trade.profit
            for trade in self.winning_trades()
        )

    def gross_loss(self):
        return sum(
            trade.profit
            for trade in self.losing_trades()
        )

    def profit_factor(self):
        gross_profit = self.gross_profit()
        gross_loss = abs(self.gross_loss())

        if gross_loss == 0:
            return float('inf')

        return gross_profit / gross_loss

    def average_duration(self):
        if not self.completed_trades:
            return 0

        total_duration = sum(
            (
                trade.exit_timestamp - trade.entry_timestamp
                for trade in self.completed_trades
            ),
            self.completed_trades[0].exit_timestamp
            - self.completed_trades[0].exit_timestamp
        )

        return total_duration / len(self.completed_trades)

    def shortest_duration(self):
        if not self.completed_trades:
            return None

        return min(
            trade.exit_timestamp - trade.entry_timestamp
            for trade in self.completed_trades
        )

    def longest_duration(self):
        if not self.completed_trades:
            return None

        return max(
            trade.exit_timestamp - trade.entry_timestamp
            for trade in self.completed_trades
        )

    def total_profit(self):
        return sum(
            trade.profit
            for trade in self.completed_trades
        )

    def average_return_pct(self):
        if not self.completed_trades:
            return 0

        return mean(
            trade.return_pct
            for trade in self.completed_trades
        )

    def best_return_pct(self):
        if not self.completed_trades:
            return 0

        return max(
            trade.return_pct
            for trade in self.completed_trades
        )

    def worst_return_pct(self):
        if not self.completed_trades:
            return 0

        return min(
            trade.return_pct
            for trade in self.completed_trades
        )

    def print_summary(self):
        print()
        print('Trade Analysis')
        print('--------------')
        print(f'Completed trades: {self.trade_count()}')
        print(f'Winning trades:   {len(self.winning_trades())}')
        print(f'Losing trades:    {len(self.losing_trades())}')
        print(f'Win rate:         {self.win_rate():.2%}')
        print()

        print(f'Average profit:   ${self.average_profit():.2f}')
        print(f'Median profit:    ${self.median_profit():.2f}')
        print(f'Average win:      ${self.average_win():.2f}')
        print(f'Average loss:     ${self.average_loss():.2f}')
        print(f'Largest win:      ${self.largest_win():.2f}')
        print(f'Largest loss:     ${self.largest_loss():.2f}')
        print()

        print(f'Gross profit:     ${self.gross_profit():.2f}')
        print(f'Gross loss:      ${self.gross_loss():.2f}')
        print(f'Profit factor:    {self.profit_factor():.2f}')
        print(f'Total profit:     ${self.total_profit():.2f}')
        print()

        print(f'Average return:   {self.average_return_pct():.2%}')
        print(f'Best return:      {self.best_return_pct():.2%}')
        print(f'Worst return:     {self.worst_return_pct():.2%}')
        print()

        average_duration = self.average_duration()

        print(
            f'Average duration: {average_duration}'
        )
        print(
            f'Shortest trade:   {self.shortest_duration()}'
        )
        print(
            f'Longest trade:    {self.longest_duration()}'
        )
        
    def print_trades(self):
        print()
        print('Completed Trades')
        print('-----------------')

        for number, trade in enumerate(
            self.completed_trades,
            start=1
        ):
            duration = (
                trade.exit_timestamp -
                trade.entry_timestamp
            )

            print(
                f'{number:>2}. '
                f'{trade.entry_timestamp} → '
                f'{trade.exit_timestamp} | '
                f'{duration} | '
                f'P&L: ${trade.profit:.2f} | '
                f'Return: {trade.return_pct:.2%}'
            )
