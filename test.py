import asyncio
import time
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
from ta import momentum, trend
import openpyxl


def get_candels(ticker, timeframe):
    """Забираем свечи с binance"""

    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=100)

    return result


def calculation_ema(close, window=5):
    """
    Формирование EMA
    и добавление нового столбца в DataFrame Pandas ["ema"]
    """
    ema_object = trend.EMAIndicator(close, window, fillna=True)
    ema = ema_object.ema_indicator()

    return ema.round(4)


def calculation_tsi(close, longlen=20, shortlen=5):
    """
    Формирование Stochastic Oscillator и его сигнала
    добавление нового столбца в DataFrame Pandas ["tsi"]
    """
    tsi_object = momentum.tsi(close, window_slow=longlen, window_fast=shortlen, fillna=True) / 100

    return tsi_object.round(4)


def calculation_signal(tsi, ema):
    """Формирование сигнала гистограммы"""
    signal = tsi - ema

    return signal.round(4)


def determining_the_position(data):
    """
    Определение позиции
    result["signal"] > 0 -> position_signal (1)
    result["signal"] < 0 -> position_signal (0)
    """
    position_signal = []

    for i in range(0, len(data)):
        try:
            if data[i] > 0:
                position_signal.append(1)
            else:
                position_signal.append(0)
        except KeyError:
            position_signal.append(np.nan)

    return position_signal


def creating_dataframe(candles):
    """Формирование полученных свечей в DataFrame"""
    dates = []
    close_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%d.%m.%Y %H:%M'))
        close_data.append(candle[4])

    result = pd.DataFrame(data={
        'dates': dates,
        'close': close_data,
    })

    result['tsi'] = calculation_tsi(result['close'])
    result['ema'] = calculation_ema(result['tsi'])
    result['signal'] = calculation_signal(result['tsi'], result['ema'])
    result['position'] = determining_the_position(result['signal'])

    table = list(filter(lambda x: x == 0, result['position']))
    print(table)

    # print(f'\ndataframe:\n{result}\n')
    result.to_excel('test.xlsx')


    return result


def main():
    start_time = time.perf_counter()
    symbols = ['BTC/USDT',]
    timeframes = ['6h',]
    
    try:
        for symbol in symbols:
            for timeframe in timeframes:
                candles = get_candels(symbol, timeframe)
                dataframe = creating_dataframe(candles)
                print(f'Symbol: {symbol} | Timeframe: {timeframe} | Status: Ok!')
    except Exception as err:
        print(f'Symbol: {symbol} | Timeframe: {timeframe} | Status: Error - {err.__str__()}')

    print(f'\nFinish: {time.perf_counter() - start_time}\n')


if __name__ == '__main__':
    main()
    