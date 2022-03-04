import ccxt
import pandas as pd
import numpy as np

# numbers = np.arange(10)
# res = list(filter(lambda x: x % 2 != 0, numbers))
# print(res)


class CorrectionTable:
    """Summary tables on ATH correction

    From: https://bytwork.com/articles/ath

    This is the highest price value for the entire existence of the cryptocurrency.
    This indicator shows how much the price of a certain cryptocurrency or coin has
    fallen as a percentage. This percentage shows how much the coin has
    fallen from its recorded historical maximum.

    Args:
        exchange(list): dataset 'Exchange' column.
        symbol(list): dataset 'Symbol' column.
        timeframe(str): dataset 'Timeframe' string.
    """

    def __init__(
            self,
            exchange: str,
            symbol: list,
            timeframe: str = '1h',
    ):
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe

    def create_dataframe(self):
        pass


def get_candles(symbol, timeframe):
    """Taking candles from binance"""
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(symbol, timeframe, limit=26)

    return result


def main():
    pass


if __name__ == '__main__':
    main()
