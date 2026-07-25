from pathlib import Path
import pandas as pd

class CacheManager:
    def __init__(self, root='historical_data'):
        self.root = Path(root)
        
    def exists(
        self,
        asset_type,
        timeframe,
        symbol
    ):
        return self._get_file_path(
            asset_type,
            timeframe,
            symbol
        ).exists()

    def load(
        self,
        asset_type,
        timeframe,
        symbol
    ):
        path = self._get_file_path(
            asset_type,
            timeframe,
            symbol
        )

        return pd.read_parquet(path)

    def save(
        self,
        df,
        asset_type,
        timeframe,
        symbol
    ):
        path = self._get_file_path(
            asset_type,
            timeframe,
            symbol
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(path)

    def last_timestamp(
        self,
        asset_type,
        timeframe,
        symbol
    ):
        if not self.exists(
            asset_type,
            timeframe,
            symbol
        ):
            return None

        df = self.load(
            asset_type,
            timeframe,
            symbol
        )

        if df.empty:
            return None

        return df.index.max()     
        
    def _get_file_path(
        self,
        asset_type,
        timeframe,
        symbol
    ):
        safe_symbol = symbol.replace('/', '_')
        return (
            self.root
            / asset_type
            / timeframe.folder
            / f'{safe_symbol}.parquet'
        )
