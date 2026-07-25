import os
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

from alpaca.data.historical import (
    StockHistoricalDataClient,
    CryptoHistoricalDataClient,
)

from downloader.alpaca_downloader import AlpacaDownloader
from downloader.cache_manager import CacheManager
from downloader.download_manager import DownloadManager
from data.data_processor import DataProcessor
from data.validators import validate_data
from utils.api_metrics import ApiMetrics
from utils.timeframe import Timeframe

# Settings
asset_type = 'crypto'
symbols = ['BTC/USD']
timeframe = Timeframe.MINUTE 
start = datetime(2024, 1, 1, tzinfo=ZoneInfo('UTC'))  
end = datetime(2024, 1, 2, tzinfo=ZoneInfo('UTC'))

def main():
    print('\n🚀 Initializing Historical Downloader...\n')
    load_dotenv()
    api_metrics = ApiMetrics()
    API_KEY = os.getenv('ALPACA_API_KEY')
    SECRET_KEY = os.getenv('ALPACA_SECRET_KEY') 

    stock_client = StockHistoricalDataClient(
        API_KEY,
        SECRET_KEY
    )

    crypto_client = CryptoHistoricalDataClient(
        API_KEY,
        SECRET_KEY
    )

    downloader = AlpacaDownloader(
        stock_client=stock_client,
        crypto_client=crypto_client,
        api_metrics=api_metrics,
    )

    cache = CacheManager()
    manager = DownloadManager(
        downloader=downloader,
        cache_manager=cache,
    )
    
    processor = DataProcessor(timeframe)    

    data = manager.get_data(
        asset_type=asset_type,
        symbols=symbols,
        timeframe=timeframe,
        start=start,
        end=end,
    )
    
    print('\n✅ Download Complete')   
    
    for symbol, df in data.items():
        validate_data(
            df,
            symbol
        )

        processed_df = processor.process(df)
        print(
            f'{symbol} processed rows: '
            f'{len(processed_df)}'
        )    

if __name__ == '__main__':
    main()
