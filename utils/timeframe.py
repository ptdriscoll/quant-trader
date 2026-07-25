from enum import Enum
from alpaca.data.timeframe import TimeFrame

class Timeframe(Enum):
    MINUTE = ('1Min', 1)
    HOUR = ('1Hour', 60)
    DAY = ('1Day', 1440)

    @property
    def folder(self):
        return self.value[0]

    @property
    def minutes(self):
        return self.value[1]
        
    @property
    def alpaca(self):
        return {
            Timeframe.MINUTE: TimeFrame.Minute,
            Timeframe.HOUR: TimeFrame.Hour,
            Timeframe.DAY: TimeFrame.Day,
        }[self]        

    def __str__(self):
        return self.folder
