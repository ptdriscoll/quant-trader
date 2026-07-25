from enum import Enum
from dataclasses import dataclass

@dataclass(frozen=True)
class TimeframeInfo:
    folder: str
    minutes: int
    pandas_freq: str

class Timeframe(Enum):
    MINUTE = TimeframeInfo(
        folder='1Min',
        minutes=1,
        pandas_freq='1min'
    )

    HOUR = TimeframeInfo(
        folder='1Hour',
        minutes=60,
        pandas_freq='1h'
    )

    DAY = TimeframeInfo(
        folder='1Day',
        minutes=1440,
        pandas_freq='1D'
    )

    @property
    def folder(self):
        return self.value.folder

    @property
    def minutes(self):
        return self.value.minutes
        
    @property
    def pandas_freq(self):
        return self.value.pandas_freq       

    def __str__(self):
        return self.folder
