from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    timestamp: datetime
    symbol: str
    side: str
    quantity: float
    market_price: float
    execution_price: float
    fee: float

    @property
    def slippage(self):
        if self.side == 'BUY':
            return (
                self.execution_price - self.market_price
            ) * self.quantity

        return (
            self.market_price - self.execution_price
        ) * self.quantity

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
    entry_slippage: float
    exit_slippage: float

    @property
    def gross_profit(self):
        return (
            self.exit_price - self.entry_price
        ) * self.quantity

    @property
    def total_fees(self):
        return self.entry_fee + self.exit_fee

    @property
    def total_slippage(self):
        return (
            self.entry_slippage +
            self.exit_slippage
        )

    @property
    def profit_before_costs(self):
        return (
            self.gross_profit +
            self.total_slippage
        )

    @property
    def profit(self):
        return (
            self.gross_profit -
            self.entry_fee -
            self.exit_fee
        )

    @property
    def return_pct(self):
        return self.profit / (
            self.entry_price * self.quantity
        )
