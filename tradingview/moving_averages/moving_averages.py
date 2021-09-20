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

def ema_indicator(data, window):
    '''Расчет EMA'''
    ema_number = trend.EMAIndicator(data, window, fillna=True).ema_indicator()

    return ema_number.round(4)

def get_candels_dataframe(ticker, timeframe):
    '''Формирование полученных свечей в DataFrame'''
    candles = get_candels(ticker, timeframe)

    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%d-%m-%Y %H:%M'))
        # open_data.append(candle[1])
        # high_data.append(candle[2])
        # low_data.append(candle[3])
        close_data.append(candle[4])
        # volume_data.append(candle[5])

    result = pd.DataFrame(data={
        'dates': dates,
        # 'open': open_data,
        # 'high': high_data,
        # 'low': low_data,
        'close': close_data,
        # 'volume': volume_data,
    })

    return result

def color_detection(data):
    '''Определение ПОКУПКА/ПРОДАЖА'''
    color_ao = []
    color_ao.append(1)
    for i in range(1, len(data)):
        if data[i - 1] > data[i]:
            color_ao.append('Вниз')
        else:
            color_ao.append('Вверх')

    return color_ao

def ema_and_color(ticker, timeframe):
    '''Заполнение DataFrame'''
    ema_periods = [3, 7, 9, 14, 18, 21, 26, 30, 40, 50, 64, 75, 90, 100, 120, 150, 180, 200]
    result = get_candels_dataframe(ticker, timeframe)

    for ema_period in ema_periods:
        result[f'{ema_period}'] = ema_indicator(result['close'], ema_period)
        result[f'color({ema_period})'] = color_detection(result[f'{ema_period}'])
    
    result.to_excel('filling.xlsx')
    return result

def trend_3_21(ticker, timeframe):
    '''Вывод значение для таблицы от 3 до 21'''
    result = ema_and_color(ticker, timeframe).tail(2).head(1).reset_index(drop=True)
    trend = []

    for key in result.loc[:, '3':'color(21)']:
        trend.append(result[f'{key}'][0])

    return trend

def trend_26_75(ticker, timeframe):
    '''Вывод значение для таблицы от 26 до 75'''
    result = ema_and_color(ticker, timeframe).tail(2).head(1).reset_index(drop=True)
    trend = []

    for key in result.loc[:, '26':'color(75)']:
        trend.append(result[f'{key}'][0])

    return trend

def trend_90_200(ticker, timeframe):
    '''Вывод значение для таблицы от 90 до 200'''
    result = ema_and_color(ticker, timeframe).tail(2).head(1).reset_index(drop=True)
    trend = []

    for key in result.loc[:, '90':'color(200)']:
        trend.append(result[f'{key}'][0])

    return trend

def create_trend(ticker, timeframe):
    '''Группировка всех таблиц, вывод таблицы по всем значениям'''
    result = ema_and_color(ticker, timeframe).tail(2).head(1).reset_index(drop=True)
    trend = []

    trend.append(ticker)
    trend.append(timeframe)

    for key in result.loc[:, '3':'color(200)']:
        trend.append(result[f'{key}'][0])

    return trend

def main():
    '''Главный метод вызывающий остальные'''
    tickers = ['BTC/USDT']
    timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    # timeframes = ['15m']

    for ticker in tickers:
        print(colored(f'ticker = {ticker}', 'green', attrs=['bold']))
        for timeframe in timeframes:
            print(colored(f'\n-----------------------------------------------------', 'blue', attrs=['bold']))
            print(colored(f'timeframe = {timeframe}', 'blue', attrs=['bold']))
            line1 = trend_3_21(ticker, timeframe)
            line2 = trend_26_75(ticker, timeframe)
            line3 = trend_90_200(ticker, timeframe)
            trend = create_trend(ticker, timeframe)

            print(colored(f'trend_3_21', 'magenta', attrs=['bold']))
            print(line1)
            print(colored(f'trend_26_75', 'magenta', attrs=['bold']))
            print(line2)
            print(colored(f'trend_90_200', 'magenta', attrs=['bold']))
            print(line3)
            print(colored(f'TREND', 'yellow', attrs=['bold']))
            print(trend)

if __name__ == "__main__":
    result = main()