from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    timestamp: datetime
    symbol: str
    side: str
    quantity: float
    price: float

@dataclass
class CompletedTrade:
    entry_timestamp: datetime
    exit_timestamp: datetime
    symbol: str
    quantity: float
    entry_price: float
    exit_price: float

    @property
    def profit(self):
        return (
            self.exit_price - self.entry_price
        ) * self.quantity

    @property
    def return_pct(self):
        return (
            self.exit_price / self.entry_price
        ) - 1
