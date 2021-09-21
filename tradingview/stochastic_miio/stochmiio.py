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

def stoch_rsi(close, window=20, smooth1=5, smooth2=5):
    '''Расчет StochRSIIndicator'''
    stoch = momentum.StochRSIIndicator(close, window, smooth1, smooth2, fillna=True)
    stochrsi = stoch.stochrsi()
    lineK = stoch.stochrsi_k()
    lineD = stoch.stochrsi_d()

    return stochrsi, lineK, lineD

def rsi_indicator(close, window=10):
    '''Расчет StochasticOscillator'''
    stoch = momentum.RSIIndicator(close, window, fillna=True)
    rsi = stoch.rsi()

    return rsi

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

    signal = rsi_indicator(result['close'])
    result['signal'] = signal
    # -----------------------------------------------------
    srsi, line_k, line_d = stoch_rsi(result['signal'])
    result['srsi'] = srsi
    result['%k'] = line_k
    result['%d'] = line_d


    
    # result.to_excel('with_srsi.xlsx')

    return result

def main():
    '''Главный метод вызывающий остальные'''
    tickers = ['BTC/USDT']
    # timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    timeframes = ['15m']

    for ticker in tickers:
        print(colored(f'ticker = {ticker}', 'green', attrs=['bold']))
        for timeframe in timeframes:
            print(colored(f'\n-----------------------------------------------------', 'blue', attrs=['bold']))
            print(colored(f'timeframe = {timeframe}', 'blue', attrs=['bold']))
            trend = get_candels_dataframe(ticker, timeframe)
            print(f'trend\n{trend}')

if __name__ == "__main__":
    main()