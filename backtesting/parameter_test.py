from backtesting.backtest_engine import BacktestEngine
from backtesting.performance import Performance
from strategies.crypto_strategy import CryptoStrategy
from signals.moving_average_cross_signal import MovingAverageCrossSignal
from risk.fixed_stop_loss_risk import FixedStopLossRisk

class ParameterSweep:
    def __init__(
        self,
        data,
        symbol,
        initial_cash=10000,
        sort=None        
    ):
        self.data = data
        self.symbol = symbol
        self.initial_cash = initial_cash
        self.sort = sort         

    def run(
        self,
        fast_types,
        fast_lengths,
        slow_types,
        slow_lengths
    ):
        results = []

        for fast_type in fast_types:
            for fast_length in fast_lengths:
                for slow_type in slow_types:
                    for slow_length in slow_lengths:
                    
                        if fast_length >= slow_length:
                            continue

                        signal = MovingAverageCrossSignal(
                            fast_type=fast_type,
                            fast_length=fast_length,
                            slow_type=slow_type,
                            slow_length=slow_length
                        )

                        strategy = CryptoStrategy(
                            trading_client=None,
                            data_client=None,
                            api_metrics=None,
                            signal=signal,
                            risk=FixedStopLossRisk()
                        )

                        engine = BacktestEngine(
                            data=self.data,
                            strategy=strategy,
                            symbol=self.symbol,
                            initial_cash=self.initial_cash
                        )

                        engine.run(verbose=False)

                        performance = Performance(
                            initial_cash=engine.initial_cash,
                            equity_curve=engine.equity_curve,
                            trades=engine.trades,
                            completed_trades=engine.completed_trades
                        )

                        results.append(
                            {
                                'fast_type': fast_type,
                                'fast_length': fast_length,
                                'slow_type': slow_type,
                                'slow_length': slow_length,
                                'final_value': performance.final_value(),
                                'return': performance.total_return(),
                                'max_drawdown': (performance.max_drawdown()),
                                'trades': performance.trade_count(),
                                'completed_trades': (performance.completed_trade_count()),
                                'profit_factor': (performance.profit_factor())
                            }
                        )
        
        if self.sort:    
            results.sort(
                key=lambda result: result[self.sort],
                reverse=True
            )

        return results
