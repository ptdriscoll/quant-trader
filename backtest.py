import pandas as pd

from utils.timeframe import Timeframe
from data.data_processor import DataProcessor
from backtesting.backtest_engine import BacktestEngine

from strategies.crypto_strategy import CryptoStrategy
from signals.moving_average_cross_signal import MovingAverageCrossSignal
from risk.fixed_stop_loss_risk import FixedStopLossRisk

from backtesting.performance import Performance
from backtesting.benchmark import BuyAndHoldBenchmark

def main():
    # Load historical data
    raw_df = pd.read_parquet('historical_data/crypto/1Min/BTC_USD.parquet')

    # Process data
    processor = DataProcessor(Timeframe.MINUTE)
    processed_df = processor.process(raw_df)

    # Create strategy
    strategy = CryptoStrategy(
        trading_client=None,
        data_client=None,
        api_metrics=None,
        signal=MovingAverageCrossSignal(),
        risk=FixedStopLossRisk()
    )

    # Create engine
    engine = BacktestEngine(
        data=processed_df,
        strategy=strategy,
        symbol='BTC/USD'
    )

    # Run
    engine.run()
    
    performance = Performance(
        initial_cash=10000,
        equity_curve=engine.equity_curve,
        trades=engine.trades,
        completed_trades=engine.completed_trades
    )
    
    print()
    print('Completed Trade Performance')
    print(
        f'Profit before costs: '
        f'${performance.completed_trade_profit_before_costs():,.2f}'
    )
    print(
        f'Slippage cost: '
        f'-${performance.total_slippage():,.2f}'
    )
    print(
        f'Fees: '
        f'-${performance.total_fees():,.2f}'
    )
    print(
        f'Net trade profit: '
        f'${performance.completed_trade_profit():,.2f}'
    )

    print()
    print('Portfolio Performance')
    print(
        f'Final portfolio value: '
        f'${performance.final_value():,.2f}'
    )
    print(
        f'Total profit: '
        f'${performance.total_profit():,.2f}'
    )
    print(
        f'Open position P&L: '
        f'${performance.open_position_profit():,.2f}'
    )    
    print(
        f'Total return: '
        f'{performance.total_return():.2%}'
    )
    print(
        f'Executions: '
        f'{performance.trade_count()}'
    )
    print(
        f'Completed trades: '
        f'{performance.completed_trade_count()}'
    )
    print(
        f'Win rate: '
        f'{performance.win_rate():.2%}'
    )
    print(
        f'Average win: '
        f'${performance.average_win():,.2f}'
    )
    print(
        f'Average loss: '
        f'${performance.average_loss():,.2f}'
    )
    print(
        f'Profit factor: '
        f'{performance.profit_factor():.2f}'
    )
    print(
        f'Max drawdown: '
        f'{performance.max_drawdown():.2%}'
    )   

    # Show benchmarks
    benchmark = BuyAndHoldBenchmark(initial_cash=10_000)
    benchmark_result = benchmark.run(processed_df)
    benchmark_performance = Performance(
        initial_cash=10_000,
        equity_curve=benchmark_result['equity_curve'],
        trades=[],
        completed_trades=[]
    )
    
    print()
    print('Buy & Hold Benchmark')
    print(
        f'Final portfolio value: '
        f'${benchmark_result["final_value"]:,.2f}'
    )
    print(
        f'Total profit: '
        f'${benchmark_result["total_profit"]:,.2f}'
    )
    print(
        f'Total return: '
        f'{benchmark_result["total_return"]:.2%}'
    )
    print(
        f'Max drawdown: '
        f'{benchmark_performance.max_drawdown():.2%}'
    )     

if __name__ == '__main__':
    main()
