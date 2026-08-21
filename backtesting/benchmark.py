class BuyAndHoldBenchmark:
    def __init__(self, initial_cash):
        self.initial_cash = initial_cash

    def run(self, data):
        if data.empty:
            return {
                'final_value': self.initial_cash,
                'total_profit': 0,
                'total_return': 0,
                'equity_curve': [],
            }

        entry_price = data['close'].iloc[0]
        quantity = self.initial_cash / entry_price
        equity_curve = []

        for timestamp, row in data.iterrows():
            portfolio_value = quantity * row['close']
            
            equity_curve.append(
                {
                    'timestamp': timestamp,
                    'portfolio_value': portfolio_value,
                }
            )

        final_value = equity_curve[-1]['portfolio_value']
        total_profit = final_value - self.initial_cash
        total_return = total_profit / self.initial_cash

        return {
            'final_value': final_value,
            'total_profit': total_profit,
            'total_return': total_return,
            'equity_curve': equity_curve,
        }
