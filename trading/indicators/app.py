import ccxt
import logging
import datetime
import pandas as pd
import numpy as np
from ta import momentum, trend, volatility

from trading import indicators, copy

# Logging Confige
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')


def get_candles(symbol: str = 'BTC/USDT', timeframe: str = '1h') -> list:
    """We get candles with ByBit"""
    bybit = ccxt.bybit()
    result = bybit.fetch_ohlcv(symbol, timeframe, limit=100)
    return result


def get_candels_dataframe(candles):
    dates = list()
    high_data = list()
    low_data = list()
    close_data = list()

    for candle in candles:
        dates.append(datetime.datetime.fromtimestamp(
            candle[0] / 1000.0).strftime('%d.%m.%Y %H:%M'))
        high_data.append(candle[2])
        low_data.append(candle[3])
        close_data.append(candle[4])

    result = pd.DataFrame(data={
        'dates': dates,
        'high': high_data,
        'low': low_data,
        'close': close_data,
    })
    return result


def main():
    candles = get_candles()
    df_candles = get_candels_dataframe(candles)
    df_candles['atr'] = copy.ADX(df_candles['high'], df_candles['low'], df_candles['close'])
    print(df_candles.tail(5))
    df_candles.to_excel('df_candles.xlsx')


if __name__ == '__main__':
    main()
