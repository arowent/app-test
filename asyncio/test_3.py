import asyncio
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
from termcolor import colored
import time


def get_candles(ticker, timeframe):
    """Забираем свечи с binance"""
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=500)

    return result


def get_candels_dataframe(ticker, timeframe):
    """Формирование полученных свечей в DataFrame"""
    candles = get_candels(ticker, timeframe)

    dates = []
    close_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%d-%m-%Y %H:%M'))
        close_data.append(candle[4])

    result = pd.DataFrame(data={
        'dates': dates,
        'close': close_data,
    })

    return result


def main():
    """Главный метод вызывающий остальные"""
    tickers = ['BTC/USDT']
    # timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    timeframes = ['5m']

    for ticker in tickers:
        for timeframe in timeframes:
            print(colored(f'ticker = {ticker}', 'green', attrs=['bold']))
            print(colored(f'timeframe = {timeframe}', 'blue', attrs=['bold']))
            trend = get_candels_dataframe(ticker, timeframe)
            # print(f'\ncreate_table:\n{trend}')


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    print(colored(f'\nFINISH: {time.perf_counter() - start_time}', 'yellow', attrs=['bold']))
