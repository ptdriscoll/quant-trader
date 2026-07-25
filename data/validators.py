def validate_data(df, symbol=None):
    print('\n📊 Data Validation')

    if symbol:
        print(f'Symbol: {symbol}')

    print(f'Rows: {len(df)}')
    print(f'Start: {df.index.min()}')
    print(f'End: {df.index.max()}')

    print(
        f'Duplicates: '
        f'{df.index.duplicated().sum()}'
    )

    print(
        f'Sorted: '
        f'{df.index.is_monotonic_increasing}'
    )

    missing_values = df.isna().sum().sum()

    print(
        f'Missing values: '
        f'{missing_values}'
    )

    print('---------------------')
