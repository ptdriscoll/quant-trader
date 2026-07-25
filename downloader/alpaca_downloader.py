import pandas as pd
from utils.timeframe import Timeframe

from alpaca.data.requests import (
    StockBarsRequest,
    CryptoBarsRequest,
)

from downloader.base_downloader import BaseDownloader

class AlpacaDownloader(BaseDownloader):
    def __init__(
        self,
        stock_client,
        crypto_client,
        api_metrics,
    ):
        self.stock_client = stock_client
        self.crypto_client = crypto_client
        self.api_metrics = api_metrics

    def download(
        self,
        asset_type,
        symbols,
        timeframe,
        start,
        end,
    ):      
        if asset_type == 'crypto':
            request = CryptoBarsRequest(
                symbol_or_symbols=symbols,
                timeframe=timeframe.alpaca,
                start=start,
                end=end,
            )

            self.api_metrics.record_request('get_crypto_bars')
            bars = self.crypto_client.get_crypto_bars(request)

        elif asset_type == 'equity':
            request = StockBarsRequest(
                symbol_or_symbols=symbols,
                timeframe=timeframe.alpaca,
                start=start,
                end=end,
            )

            self.api_metrics.record_request('get_stock_bars')
            bars = self.stock_client.get_stock_bars(request)

        else:
            raise ValueError(
                f'Unknown asset type: {asset_type}'
            )

        if bars.df.empty:
            return {}

        data = {}
        master_df = bars.df
        for symbol in symbols:

            try:
                data[symbol] = master_df.loc[symbol].copy()

            except KeyError:

                print(
                    f'⚠️ No data returned for {symbol}.'
                )

        return data
