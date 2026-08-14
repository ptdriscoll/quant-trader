import pandas as pd

from utils.timeframe import Timeframe
from data.data_processor import DataProcessor
from backtesting.backtest_engine import BacktestEngine

from strategies.crypto_strategy import CryptoStrategy
from signals.moving_average_cross_signal import MovingAverageCrossSignal
from risk.fixed_stop_loss_risk import FixedStopLossRisk
from backtesting.performance import Performance

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
    print(
        f'Final portfolio value: '
        f'${performance.final_value():,.2f}'
    )
    print(
        f'Total profit: '
        f'${performance.total_profit():,.2f}'
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

if __name__ == '__main__':
    main()
