from utils.fee_model import FEE_MODEL

class SimulatedBroker:
    def __init__(
        self,
        portfolio,
        asset_type='crypto'
    ):
        self.portfolio = portfolio
        self.asset_type = asset_type
        self.fees = FEE_MODEL[asset_type]

    def buy(
        self,
        symbol,
        quantity,
        price,
        verbose=True
    ):
        execution_price = (price * (1 + self.fees['slippage_pct']))
        gross_value = (quantity * execution_price)
        fee = self._buy_fee(gross_value)

        self.portfolio.buy(
            symbol,
            quantity,
            execution_price,
            fee
        )
        
        if verbose:
            print(
                f'\nBUY execution: '
                f'market={price:.4f} '
                f'execution={execution_price:.4f} '
                f'fee=${fee:.2f}'
            )        

        return {
            'price': execution_price,
            'fee': fee,
        }

    def sell(
        self,
        symbol,
        quantity,
        price,
        verbose=True
    ):
        execution_price = (price * (1 - self.fees['slippage_pct']))
        gross_value = (quantity * execution_price)
        fee = self._sell_fee(gross_value)
        self.portfolio.sell(symbol, execution_price, fee)
        
        if verbose:
            print(
                f'\nSELL execution: '
                f'market={price:.4f} '
                f'execution={execution_price:.4f} '
                f'fee=${fee:.2f}'
            )        

        return {
            'price': execution_price,
            'fee': fee,
        }

    def _buy_fee(self, gross_value):
        if self.asset_type == 'crypto':
            return (gross_value * self.fees['taker_fee_pct'])

        return 0

    def _sell_fee(self, gross_value):
        if self.asset_type == 'crypto':
            return (gross_value * self.fees['taker_fee_pct'])

        return (
            gross_value
            * self.fees['reg_fee_per_sell']
        )
