import pandas as pd

from utils.timeframe import Timeframe
from data.data_processor import DataProcessor
from backtesting.backtest_engine import BacktestEngine

from strategies.crypto_strategy import CryptoStrategy
from signals.moving_average_cross_signal import MovingAverageCrossSignal
from risk.fixed_stop_loss_risk import FixedStopLossRisk

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
    
    print()
    print(f'Trades: {len(engine.trades)}')
    print(
        f'Final portfolio value: '
        f'${engine.equity_curve[-1]["portfolio_value"]:,.2f}'
    )

if __name__ == '__main__':
    main()
