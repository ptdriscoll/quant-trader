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
from utils.api_metrics import ApiMetrics
from utils.timeframe import Timeframe

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

    data = manager.get_data(
        asset_type='crypto',
        symbols=['BTC/USD'],
        timeframe=Timeframe.MINUTE,
        start=datetime(
            2024,
            1,
            1,
            tzinfo=ZoneInfo('UTC')
        ),
        end=datetime(
            2024,
            1,
            2,
            tzinfo=ZoneInfo('UTC')
        ),
    )

    print('\n✅ Download Complete')
    for symbol, df in data.items():
        print(f'\n{symbol}')
        print(df.head())
        print(df.tail())
        print(f'\nRows: {len(df)}')
        print(f'Start: {df.index.min()}')
        print(f'End: {df.index.max()}')
        print(f'Missing minutes: {1440 - len(df)}')


if __name__ == '__main__':
    main()
