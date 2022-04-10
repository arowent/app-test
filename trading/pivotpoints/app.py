from unicodedata import name
import ccxt
import logging
import datetime
import pandas as pd
import numpy as np
from ta import trend, momentum, volatility
from pivotpoints import fibonacci

from pivotpoints.fibonacci import Fibonacci
# from pivotpoints import tools

# Logging Confige
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')


def get_candles(symbol: str = 'BTC/USDT', timeframe: str = '1h') -> list:
    """We get candles with ByBit"""
    bybit = ccxt.bybit()
    result = bybit.fetch_ohlcv(symbol, timeframe, limit=200)
    return result


def get_candels_dataframe(candles):
    timestamp = list()
    high_data = list()
    low_data = list()
    close_data = list()

    for candle in candles:
        timestamp.append(candle[0])
        high_data.append(candle[2])
        low_data.append(candle[3])
        close_data.append(candle[4])

    result = pd.DataFrame(data={
        'timestamp': timestamp,
        'high': high_data,
        'low': low_data,
        'close': close_data,
    })
    # result['position'] = result['ao'].apply(lambda x: 1 if x > 0 else 0)
    return result


def main():
    candles = get_candles()
    df_candles = get_candels_dataframe(candles)
    result = Fibonacci(df_candles).fibonacci()
    df_candles.to_excel('df_candles.xlsx')
    print(f'result: {result}')


if __name__ == '__main__':
    main()
