import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
from ta import momentum, trend
import time


def get_candels(ticker, timeframe):
    """Taking candles from binance"""

    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=500)

    return result

def get_candels_dataframe(ticker, timeframe):
    """Formation of the received candles in the DataFrame"""

    candles = get_candels(ticker, timeframe)

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
        volume_data.append(candle[5])

    result = pd.DataFrame(data={
        'dates': dates,
        'open': open_data,
        'high': high_data,
        'low': low_data,
        'close': close_data,
        'volume': volume_data,
    })

    return result


def main():
    """We get candlesticks from Finance, form a DataFrame and make calculations"""
    symbol = 'BTC/USDT'
    timeframe = '5m'
    result = None
    
    result = get_candels_dataframe(symbol, timeframe)
    print(result)

    return result



if __name__ == '__main__':
    main()