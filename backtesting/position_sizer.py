from utils.fee_model import FEE_MODEL

class PositionSizer:
    def __init__(
        self,
        risk_pct=0.95,
        asset_type='crypto'
    ):
        self.risk_pct = risk_pct
        self.asset_type = asset_type
        self.fees = FEE_MODEL[asset_type]

    def calculate_quantity(
        self,
        cash,
        price
    ):
        allocation = cash * self.risk_pct
        slippage = self.fees['slippage_pct']
        execution_price = (price * (1 + slippage))

        if self.asset_type == 'crypto':
            fee_pct = self.fees['taker_fee_pct']
        else:
            fee_pct = 0

        total_cost_multiplier = (1 + fee_pct)

        return (allocation / execution_price / total_cost_multiplier)
