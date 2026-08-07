class BaseStrategy:
    def __init__(self, signal, risk):
        self.signal = signal
        self.risk = risk

    def evaluate(self, df, position=None):
        latest_close = df['close'].iloc[-1]
        owned = position is not None
        signal = self.signal.generate(df, owned=owned)

        if owned and self.risk.evaluate(latest_close, position):
            signal = 'SELL'

        return signal
