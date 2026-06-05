from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest

class CryptoSMAStrategy:
    def __init__(self):

        self.data_client = CryptoHistoricalDataClient(
            api_key=API_KEY,
            secret_key=SECRET_KEY
        )

        self.universe = []
        
    def optimize_universe(self):
        pass
        
    def generate_signal(self):
        pass        
        
    def run(self):
        request = CryptoBarsRequest(
            symbol_or_symbols=self.universe,
            timeframe=TimeFrame.Minute,
            limit=30
        )

        bars = self.data_client.get_crypto_bars(request)    
