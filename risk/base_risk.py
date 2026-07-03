from abc import ABC, abstractmethod

class BaseRisk(ABC):
    @abstractmethod
    def evaluate(self, current_price, position):
        '''
        Returns:
            True  -> Exit the position
            False -> Hold the position
        '''
        pass
