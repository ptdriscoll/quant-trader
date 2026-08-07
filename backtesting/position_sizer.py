class PositionSizer:

    def calculate_quantity(self, cash, price):
        if price <= 0:
            return 0

        return cash / price
