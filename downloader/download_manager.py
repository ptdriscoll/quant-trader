import pandas as pd
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
        
        for symbol in symbols:
            first_cached = self.cache.first_timestamp(
                asset_type,
                timeframe,
                symbol
            )

            last_cached = self.cache.last_timestamp(
                asset_type,
                timeframe,
                symbol
            )

            # No cache: download the entire requested range.
            if first_cached is None or last_cached is None:
                print(
                    f'📥 Downloading {symbol}...'
                )

                downloaded = self._download(
                    asset_type,
                    [symbol],
                    timeframe,
                    start,
                    end,
                )

                if symbol in downloaded:
                    self.cache.save(
                        downloaded[symbol],
                        asset_type=asset_type,
                        timeframe=timeframe,
                        symbol=symbol,
                    )

                    print(
                        f'💾 Saved {symbol} to cache.'
                    )

                    results[symbol] = downloaded[symbol]

                continue

            # Requested range is already cached.
            if first_cached <= start and last_cached >= end:
                print(
                    f'💾 Loading {symbol} from cache...'
                )

                results[symbol] = self.cache.load(
                    asset_type,
                    timeframe,
                    symbol
                )

                continue

            # Download missing portions.
            cached_df = self.cache.load(
                asset_type,
                timeframe,
                symbol
            )

            downloaded_parts = []

            if start < first_cached:
                print(
                    f'📥 Downloading {symbol} '
                    f'from {start} to {first_cached}...'
                )

                downloaded = self._download(
                    asset_type,
                    [symbol],
                    timeframe,
                    start,
                    first_cached,
                )

                if symbol in downloaded:
                    downloaded_parts.append(
                        downloaded[symbol]
                    )

            if end > last_cached:
                print(
                    f'📥 Downloading {symbol} '
                    f'from {last_cached} to {end}...'
                )

                downloaded = self._download(
                    asset_type,
                    [symbol],
                    timeframe,
                    last_cached,
                    end,
                )

                if symbol in downloaded:
                    downloaded_parts.append(
                        downloaded[symbol]
                    )

            # Merge cached and newly downloaded data.
            if downloaded_parts:
                combined = (
                    [cached_df] +
                    downloaded_parts
                )

                combined_df = (
                    pd.concat(combined)
                    .sort_index()
                )

                combined_df = (
                    combined_df[
                        ~combined_df.index.duplicated(
                            keep='first'
                        )
                    ]
                )

                self.cache.save(
                    combined_df,
                    asset_type=asset_type,
                    timeframe=timeframe,
                    symbol=symbol,
                )

                print(
                    f'💾 Updated {symbol} cache.'
                )

                results[symbol] = combined_df

            else:
                results[symbol] = cached_df

        return results

    def _download(
        self,
        asset_type,
        symbols,
        timeframe,
        start,
        end,
    ):
        return self.downloader.download(
            asset_type=asset_type,
            symbols=symbols,
            timeframe=timeframe,
            start=start,
            end=end,
        )
