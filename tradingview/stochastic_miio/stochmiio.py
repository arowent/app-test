import sys
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
import ta.momentum
from termcolor import colored
from ta import momentum, trend
from logger import logger


def get_candels(ticker, timeframe):
    '''Забираем свечи с binance'''
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=500)

    return result


# def stoch_rsi(close, window, smooth1, smooth2):
#     '''Расчет StochRSIIndicator'''
#     stoch = momentum.StochRSIIndicator(close, window, smooth1, smooth2, fillna=True)
#     stochrsi = stoch.stochrsi()
#     lineK = stoch.stochrsi_k()
#     lineD = stoch.stochrsi_d()
#
#     return stochrsi, lineK, lineD

# def ema_indicator(data, window=5):
#     '''Расчет EMA'''
#     ema_number = trend.EMAIndicator(data, window, fillna=True).ema_indicator()
#
#     return ema_number
#
#     return ema_number.round(4)

def tsi_indicator(close):
    momentum_list = []
    momentum_list.append(2)
    for index in range(1, len(close)):
        moment = close[index] - close[index-1]
        momentum_list.append(moment)

    line = pd.Series(momentum_list)
    ema_numerator_one = pd.Series(ta.trend.EMAIndicator(line, 20).ema_indicator())
    ema_numerator_two = pd.Series(ta.trend.EMAIndicator(ema_numerator_one, 5).ema_indicator())
    ema_denominator_one = pd.Series(ta.trend.EMAIndicator(line, 20).ema_indicator())
    ema_denominator_two = pd.Series(abs(ta.trend.EMAIndicator(ema_denominator_one, 20).ema_indicator()))

    tsi = 100 * (ema_numerator_two/ema_denominator_two)

    return tsi

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

    # srsi, line_k, line_d = stoch_rsi(result['close'], 20, 5, 5)
    # result['srsi'] = srsi
    # result['%k'] = line_k
    # result['%d'] = line_d
    
    # stoch = stock_oscillator(result['high'], result['low'], result['close'])
    # result['signal'] = stoch

    # ema = ema_indicator(result['close'])
    # result['ema'] = ema
    #
    # tsi = strength_index(result['ema'])
    # result['tsi'] = tsi

    tsi = tsi_indicator(result['close'])
    result['tsi'] = tsi
    


    result.to_excel('with_srsi.xlsx')


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