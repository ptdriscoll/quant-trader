class SimulatedBroker:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def buy(self, symbol, quantity, price):
        self.portfolio.buy(symbol, quantity, price)

    def sell(self, symbol, price):
        self.portfolio.sell(symbol, price)
