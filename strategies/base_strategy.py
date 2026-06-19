class BaseStrategy:
    def optimize_universe(self):
        raise NotImplementedError

    def is_active(self):
        raise NotImplementedError
        
    def run(self):
        raise NotImplementedError
