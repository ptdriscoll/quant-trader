from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    timestamp: datetime
    symbol: str
    side: str
    quantity: float
    price: float
    fee: float = 0

@dataclass
class CompletedTrade:
    entry_timestamp: datetime
    exit_timestamp: datetime
    symbol: str
    quantity: float
    entry_price: float
    exit_price: float
    entry_fee: float
    exit_fee: float
    
    @property
    def gross_profit(self):
        return (
            self.exit_price - self.entry_price
        ) * self.quantity    

    @property
    def profit(self):
        return (
            self.gross_profit
            - self.entry_fee
            - self.exit_fee
        )

    @property
    def return_pct(self):
        cost = (
            self.entry_price * self.quantity
            + self.entry_fee
        )

        if cost == 0:
            return 0

        return self.profit / cost
