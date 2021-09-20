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

    result.to_excel('pivot_points.xlsx')

    return result

def pivote_classic(Close, High, Low):
    PP = (High + Low + Close) / 3
    R1 = 2 * PP - Low
    S1 = 2 * PP - High
    R2 = PP + (High - Low)
    S2 = PP - (High - Low)
    R3 = PP + 2 * (High - Low)
    S3 = PP - 2 * (High - Low)

    pivot = []
    pivot.append(S3)
    pivot.append(S2)
    pivot.append(S1)
    pivot.append(PP)
    pivot.append(R1)
    pivot.append(R2)
    pivot.append(R3)

    return pivot

def pivot_fibonacci(Close, High, Low):
    PP = (High + Low + Close) / 3
    R1 = PP + (0.382 * (High - Low))
    S1 = PP - (0.382 * (High - Low))
    R2 = PP + (0.618 * (High - Low))
    S2 = PP - (0.618 * (High - Low))
    R3 = PP + (1.000 * (High - Low))
    S3 = PP - (1.000 * (High - Low))

    pivot = []
    pivot.append(S3)
    pivot.append(S2)
    pivot.append(S1)
    pivot.append(PP)
    pivot.append(R1)
    pivot.append(R2)
    pivot.append(R3)

    return pivot

def pivot_camarillo(Close, High, Low):
    PP = (High + Low + Close) / 3
    R1 = Close + ((High - Low) * 1.0833)
    S1 = Close - ((High - Low) * 1.0833)
    R2 = Close + ((High - Low) * 1.1666)
    S2 = Close - ((High - Low) * 1.1666)
    R3 = Close + ((High - Low) * 1.2500)
    S3 = Close - ((High - Low) * 1.2500)

    pivot = []
    pivot.append(S3)
    pivot.append(S2)
    pivot.append(S1)
    pivot.append(PP)
    pivot.append(R1)
    pivot.append(R2)
    pivot.append(R3)

    return pivot

def pivot_woody(Close, High, Low):
    PP = (High + Low + (2 * Close)) / 4
    R1 = (2 * PP) - Low
    S1 = (2 * PP) - High
    R2 = PP + High - Low
    S2 = PP - High + Low
    R3 = "-"
    S3 = '-'

    pivot = []
    pivot.append(S3)
    pivot.append(S2)
    pivot.append(S1)
    pivot.append(PP)
    pivot.append(R1)
    pivot.append(R2)
    pivot.append(R3)

    return pivot

def pivot_de_mark(Close, High, Low, Open):
    if Close < Open:
        PP = High + (2 * Low) + Close
    elif Close > Open:
        PP = (2 * High) + Low + Close
    elif Close == Open:
        PP = High + Low + (2 * Close)

    R1 = (PP / 2) + High
    S1 = (PP / 2) - Low
    R2 = '-'
    S2 = '-'
    R3 = '-'
    S3 = '-'

    pivot = []
    pivot.append(S3)
    pivot.append(S2)
    pivot.append(S1)
    pivot.append(PP)
    pivot.append(R1)
    pivot.append(R2)
    pivot.append(R3)

    return pivot

def pivot_frame(ticker, timeframe):
    result = get_candels_dataframe(ticker, timeframe).tail(2).head(1)
    ind = result.index[0]
    print(f'IND = {ind}')
    # classic = pivote_classic(result['close'][498], result['high'][498], result['low'][498])
    classic = pivote_classic(result['close'][ind], result['high'][ind], result['low'][ind])
    fibonacci = pivot_fibonacci(result['close'][ind], result['high'][ind], result['low'][ind])
    camarillo = pivot_camarillo(result['close'][ind], result['high'][ind], result['low'][ind])
    woody = pivot_woody(result['close'][ind], result['high'][ind], result['low'][ind])
    de_mark = pivot_de_mark(result['close'][ind], result['high'][ind], result['low'][ind], result['open'][ind])

    colBase = ['S3', 'S2', 'S1', 'P', 'R1', 'R2', 'R3']
    colums = ['Точки', 'Классические', 'Фибоначчи', 'Камарилья', 'Вуди', 'ДеМарк']
    # colums = ['Точки', 'Классические']

    pivots = pd.DataFrame(zip(colBase, classic, fibonacci, camarillo, woody, de_mark), columns=colums)
    # pivots = pd.DataFrame(zip(colBase, classic), columns=colums)

    return pivots


def main():
    '''Главный метод вызывающий остальные'''
    tickers = ['BTC/USDT']
    timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    # timeframes = ['1w']

    for ticker in tickers:
        print(colored(f'ticker = {ticker}', 'green', attrs=['bold']))
        for timeframe in timeframes:
            print(colored(f'\n-----------------------------------------------------', 'blue', attrs=['bold']))
            print(colored(f'timeframe = {timeframe}', 'blue', attrs=['bold']))
            # trend = get_candels_dataframe(ticker, timeframe).tail(2).head(1)
            # print(f'trend\n{trend}')
            pp = pivot_frame(ticker, timeframe)
            print(f'pivots\n{pp}')


if __name__ == "__main__":
    main()