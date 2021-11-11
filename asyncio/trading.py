import asyncio
import time
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np


def get_candels(ticker, timeframe):
    """Забираем свечи с binance"""

    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=10)

    return result


def creating_dataframe(candles):
    """Формирование полученных свечей в DataFrame"""

    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%d-%m-%Y %H:%M'))
        open_data.append(candle[1])
        high_data.append(candle[2])
        low_data.append(candle[3])
        close_data.append(candle[4])
        # volume_data.append(candle[5])

    result = pd.DataFrame(data={
        'dates': dates,
        'open': open_data,
        'high': high_data,
        'low': low_data,
        'close': close_data,
        # 'volume': volume_data,
    })


    return result


def main():
    candles = get_candels('BTC/USDT', '6h')
    dataframe = creating_dataframe(candles)
    print(dataframe)


if __name__ == '__main__':
    main()