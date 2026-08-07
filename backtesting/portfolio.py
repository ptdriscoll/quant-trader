class Portfolio:
    def __init__(self, initial_cash):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}

    def has_position(self, symbol):
        return symbol in self.positions

    def get_position(self, symbol):
        return self.positions.get(symbol)

    def buy(self, symbol, quantity, price):
        cost = quantity * price
        if cost > self.cash:
            raise ValueError(
                f'Insufficient cash to buy {quantity} '
                f'{symbol} at {price}.'
            )

        self.cash -= cost

        self.positions[symbol] = {
            'quantity': quantity,
            'entry_price': price,
        }

    def sell(self, symbol, price):
        position = self.positions.get(symbol)
        if position is None:
            return

        proceeds = position['quantity'] * price
        self.cash += proceeds
        del self.positions[symbol]

    def market_value(self, prices):
        value = self.cash

        for symbol, position in self.positions.items():
            price = prices.get(symbol)

            if price is not None:
                value += (
                    position['quantity'] * price
                )

        return value
