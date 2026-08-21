class BuyAndHoldBenchmark:
    def __init__(self, initial_cash):
        self.initial_cash = initial_cash

    def run(self, data):
        if data.empty:
            return {
                'final_value': self.initial_cash,
                'total_profit': 0,
                'total_return': 0,
            }

        entry_price = data['close'].iloc[0]
        exit_price = data['close'].iloc[-1]

        quantity = self.initial_cash / entry_price
        final_value = quantity * exit_price

        total_profit = final_value - self.initial_cash
        total_return = total_profit / self.initial_cash

        return {
            'final_value': final_value,
            'total_profit': total_profit,
            'total_return': total_return,
        }
