from alpaca.data.timeframe import TimeFrame
from utils.timeframe import Timeframe

ALPACA_TIMEFRAMES = {
    Timeframe.MINUTE: TimeFrame.Minute,
    Timeframe.HOUR: TimeFrame.Hour,
    Timeframe.DAY: TimeFrame.Day,
}

def to_alpaca(timeframe):
    return ALPACA_TIMEFRAMES[timeframe]
