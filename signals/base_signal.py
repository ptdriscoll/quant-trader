from abc import ABC, abstractmethod

class BaseSignal(ABC):
    @property
    @abstractmethod
    def lookback(self):
        '''Number of historical bars required.'''
        pass

    @property
    @abstractmethod
    def timeframe(self):
        '''Timeframe required by this signal.'''
        pass

    @abstractmethod
    def generate(self, df, owned, position=None):
        '''
        Returns:
            'BUY'
            'SELL'
            None
        '''
        pass
