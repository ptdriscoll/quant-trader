from risk.base_risk import BaseRisk

class FixedStopLossRisk(BaseRisk):
    STOP_LOSS_PCT = 0.02

    def evaluate(self, current_price, position):
        entry_price = float(position.avg_entry_price)
        stop_price = entry_price * (1 - self.STOP_LOSS_PCT)
        return current_price <= stop_price
