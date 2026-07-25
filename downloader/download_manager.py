from downloader.cache_manager import CacheManager

class DownloadManager:
    def __init__(
        self,
        downloader,
        cache_manager,
    ):
        self.downloader = downloader
        self.cache = cache_manager

    def get_data(
        self,
        asset_type,
        symbols,
        timeframe,
        start,
        end,
    ):
        results = {}
        missing_symbols = []

        # Load everything we already have
        for symbol in symbols:
            if self.cache.exists(
                asset_type,
                timeframe,
                symbol,
            ):
                print(f'💾 Loading {symbol} from cache...')

                results[symbol] = self.cache.load(
                    asset_type,
                    timeframe,
                    symbol,
                )

            else:
                missing_symbols.append(symbol)

        # Download anything we're missing
        if missing_symbols:
            print(
                f'📥 Downloading {len(missing_symbols)} symbol(s)...'
            )

            downloaded = self.downloader.download(
                asset_type=asset_type,
                symbols=missing_symbols,
                timeframe=timeframe,
                start=start,
                end=end,
            )

            for symbol, df in downloaded.items():

                self.cache.save(
                    df,
                    asset_type=asset_type,
                    timeframe=timeframe,
                    symbol=symbol,
                )

                print(f'💾 Saved {symbol} to cache.')

                results[symbol] = df

        return results
