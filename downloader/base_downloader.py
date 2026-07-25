from abc import ABC, abstractmethod

class BaseDownloader(ABC):

    @abstractmethod
    def download(
        self,
        symbols,
        timeframe,
        start,
        end
    ):
        pass
