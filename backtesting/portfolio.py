class SimulatedPosition:
    def __init__(
        self,
        symbol,
        quantity,
        entry_price
    ):
        self.symbol = symbol
        self.quantity = quantity
        self.avg_entry_price = entry_price

class Portfolio:
    def __init__(self, initial_cash):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}

    def has_position(self, symbol):
        return symbol in self.positions

    def get_position(self, symbol):
        return self.positions.get(symbol)

    def buy(
        self,
        symbol,
        quantity,
        price,
        fee=0
    ):
        cost = quantity * price
        total_cost = cost + fee

        if total_cost > self.cash:
            raise ValueError(
                f'Insufficient cash to buy '
                f'{quantity} {symbol} at {price}.'
            )

        self.cash -= total_cost

        self.positions[symbol] = SimulatedPosition(
            symbol=symbol,
            quantity=quantity,
            entry_price=price
        )

    def sell(
        self,
        symbol,
        price,
        fee=0
    ):
        position = self.positions.get(symbol)

        if position is None:
            return

        proceeds = (position.quantity * price)
        net_proceeds = proceeds - fee
        self.cash += net_proceeds
        del self.positions[symbol]

    def market_value(self, prices):
        value = self.cash

        for symbol, position in self.positions.items():
            price = prices.get(symbol)

            if price is not None:
                value += (
                    position.quantity * price
                )

        return value
