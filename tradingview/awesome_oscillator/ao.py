import sys
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
from ta import momentum, trend
from tools import *


def get_candles(ticker, timeframe):
    """Taking candles from binance"""
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=100)

    return result


def get_candels_dataframe(candles):
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(
            candle[0] / 1000.0).strftime('%d-%m-%Y %H:%M'))
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

    result['ao'] = momentum.AwesomeOscillatorIndicator(result['high'], result['low'], 5, 34).awesome_oscillator()
    result['color'] = color_detection(result['ao'])
    result['position'] = position_determination(result['ao'])
    result['direction'] = trend_direction(result['ao'])
    result['phase'] = trend_phase(result['color'])
    result['strength'] = Strength(result['ao']).strength_ao()
    result.to_excel('./data.xlsx')
    return result


def table(data):
    result = get_candels_dataframe(data)
    print(result)


def main():
    symbols = ['BTC/USDT']
    timeframes = ['15m']

    for symbol in symbols:
        for timeframe in timeframes:
            print(f'\nsymbol: {symbol} | timeframe: {timeframe}\n')
            candles = get_candles(symbol, timeframe)
            result = table(candles)


if __name__ == '__main__':
    main()
