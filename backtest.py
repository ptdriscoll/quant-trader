import pandas as pd

from utils.timeframe import Timeframe
from data.data_processor import DataProcessor
from backtesting.backtest_engine import BacktestEngine

from strategies.crypto_strategy import CryptoStrategy
from signals.moving_average_cross_signal import MovingAverageCrossSignal
from risk.fixed_stop_loss_risk import FixedStopLossRisk

from backtesting.performance import Performance
from backtesting.benchmark import BuyAndHoldBenchmark
from backtesting.parameter_test import ParameterSweep

def main():
    # Load historical data
    raw_df = pd.read_parquet('historical_data/crypto/1Min/BTC_USD.parquet')

    # Process data
    processor = DataProcessor(Timeframe.MINUTE)
    processed_df = processor.process(raw_df)

    # Set signal
    signal = MovingAverageCrossSignal(
        fast_type='ema',
        fast_length=9,
        slow_type='sma',
        slow_length=20
    )

    # Create strategy
    strategy = CryptoStrategy(
        trading_client=None,
        data_client=None,
        api_metrics=None,
        signal=signal,
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
        initial_cash=engine.initial_cash,
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

    # Run sweep
    print()
    print('Running parameter sweep...')   

    split_index = int(len(processed_df) * 0.70)
    in_sample_data = processed_df.iloc[:split_index].copy()        
    
    sweep = ParameterSweep(
        data=in_sample_data,
        symbol='BTC/USD',
        initial_cash=10000,
        sort='return'
    )

    results = sweep.run(
        fast_types=['ema', 'sma'],
        fast_lengths=[5, 7, 9, 11, 13, 15, 17, 19],
        slow_types=['ema', 'sma'],
        slow_lengths=[20, 25, 30, 35, 40, 50, 60, 75, 100]
    )    

    selected_parameters = sweep.best_result
    if selected_parameters is None:
        raise RuntimeError('Parameter sweep produced no valid results.')

    print()
    print('Parameter Sweep Results')

    for result in results:
        print(       
            f'{result["fast_type"].upper()} '
            f'{result["fast_length"]} / '
            f'{result["slow_type"].upper()} '
            f'{result["slow_length"]}: '
            f'{result["return"]:.2%} '
            f'| DD: {result["max_drawdown"]:.2%} '
            f'| Trades: {result["trades"]} '
            f'| PF: {result["profit_factor"]:.2f}'            
        ) 

    # Run selected parameters out-of-sample
    fast_type = selected_parameters['fast_type']
    fast_length = selected_parameters['fast_length']
    slow_type = selected_parameters['slow_type']
    slow_length = selected_parameters['slow_length']

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
    
    warmup_start = split_index - signal.lookback
    out_of_sample_data = processed_df.iloc[warmup_start:].copy()

    engine = BacktestEngine(
        data=out_of_sample_data,
        strategy=strategy,
        symbol='BTC/USD',
        initial_cash=10000
    )

    engine.run(verbose=False, start_bar=signal.lookback)

    performance = Performance(
        initial_cash=engine.initial_cash,
        equity_curve=engine.equity_curve,
        trades=engine.trades,
        completed_trades=engine.completed_trades
    )

    print()
    print('Out-of-Sample Performance')
    print(
        f'Parameters: '
        f'{fast_type.upper()} {fast_length} / '
        f'{slow_type.upper()} {slow_length}'
    )
    print(
        f'Final portfolio value: '
        f'${performance.final_value():,.2f}'
    )
    print(
        f'Total return: '
        f'{performance.total_return():.2%}'
    )
    print(
        f'Max drawdown: '
        f'{performance.max_drawdown():.2%}'
    )
    print(
        f'Completed trades: '
        f'{performance.completed_trade_count()}'
    )
    print(
        f'Open position P&L: '
        f'${performance.open_position_profit():,.2f}'
    )    
    print(
        f'Profit factor: '
        f'{performance.profit_factor():.2f}'
    )        

if __name__ == '__main__':
    main()
