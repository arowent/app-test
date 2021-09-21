import sys
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
import ta.momentum
from termcolor import colored
from ta import momentum, trend

def get_candels(ticker, timeframe):
    '''Забираем свечи с binance'''
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=500)

    return result

def calculation_ema(close, window=20):
    '''
    Формирование EMA
    и добавление нового столбца в DataFrame Pandas ["ema"]
    '''
    ema_object = ta.trend.EMAIndicator(close, window)
    ema = ema_object.ema_indicator()

    return ema

def calculation_stochastic(high, low, close, window=20, smooth_window=5):
    '''
    Формирование Stochastic Oscillator и его сигнала
    добавление нового столбца в DataFrame Pandas ["stochastic"]
    '''
    stochastic_object = ta.momentum.tsi(close, window, smooth_window)
    # stochastic = stochastic_object.stoch()
    # stochastic = stochastic_object.tsi()
    # stochastic_signal = stochastic_object.stoch_signal()

    return stochastic_object

def get_candels_dataframe(ticker, timeframe):
    '''Формирование полученных свечей в DataFrame'''
    candles = get_candels(ticker, timeframe)

    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    # volume_data = []

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

    result['stochastic'] = calculation_stochastic(result['high'], result['low'], result['close'])
    result['ema'] = calculation_ema(result['close'])

    return result

def main():
    '''Главный метод вызывающий остальные'''
    tickers = ['BTC/USDT']
    # timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    timeframes = ['15m']

    for ticker in tickers:
        print(colored(f'\nticker = {ticker}', 'green', attrs=['bold']))
        for timeframe in timeframes:
            print(colored(f'-----------------------------------------------------', 'blue', attrs=['bold']))
            print(colored(f'timeframe = {timeframe}', 'blue', attrs=['bold']))
            trend = get_candels_dataframe(ticker, timeframe)
            print(f'Output of the last 5 values from "trend":\n{trend.tail(5)}')


if __name__ == "__main__":
    main()