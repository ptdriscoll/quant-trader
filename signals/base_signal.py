from abc import ABC, abstractmethod

class BaseSignal(ABC):
    LOOKBACK = 30

    @abstractmethod
    def generate(self, df, owned, position=None):
        '''
        Returns:
            'BUY'
            'SELL'
            None
        '''
        pass
