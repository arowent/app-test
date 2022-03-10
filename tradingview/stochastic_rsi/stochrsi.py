import sys
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
from ta import momentum

# from logger import logger


def get_candels(ticker, timeframe):
    binance = ccxt.bybit()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=40)

    return result


def RSI_Indicator(close, window=14):
    rsi = momentum.RSIIndicator(close, window, fillna=True).rsi()
    return rsi


def Stoch(high, low, close, window=14, smooth_window=3):
    stoch = momentum.stoch(high, low, close, window,
                           smooth_window, fillna=True)
    return stoch


def stochastic(data, window=14, k_window=3, d_window=3):
    min_val = data.rolling(window=window, center=False).min()
    max_val = data.rolling(window=window, center=False).max()

    stoch = ((data - min_val) / (max_val - min_val)) * 100

    K = stoch.rolling(window=k_window, center=False).mean()
    D = K.rolling(window=d_window, center=False).mean()

    return round(K, 6), round(D, 6)


def get_candels_dataframe(ticker, timeframe):
    candles = get_candels(ticker, timeframe)

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

    # result['stoch'] = Stoch(result['high'], result['low'], result['close'])
    result['rsi'] = RSI_Indicator(result['close'], 14)
    result['k'], result['d'] = stochastic(result['rsi'])
    # result.to_excel('candels.xlsx')
    print(result.tail(5))
    return result


def create_last_line(ticker, timeframe):
    '''Переопределяем таблицу, забираем последние 14 закрытых свечей'''
    result = get_candels_dataframe(ticker, timeframe)

    line_date = []
    line_close = []
    line_rsi = []
    line_k = []
    line_d = []

    for i in range(len(result)-2, len(result)-52, -1):
        line_date.append(result['dates'][i])
        line_close.append(result['close'][i])
        line_rsi.append(result['rsi'][i])
        line_k.append(result['k'][i])
        line_d.append(result['d'][i])

    last_line = pd.DataFrame(data={
        'dates': line_date,
        'close': line_close,
        'rsi': line_rsi,
        'k': line_k,
        'd': line_d,
    })

    last_line.to_excel('last_line.xlsx')
    return last_line


def motion(result):
    '''Определяем навправление движения Вверх/Вниз или Прямая'''

    k = ''
    d = ''

    if result['k'][0] > result['k'][1]:
        k = 'Вверх'
    elif result['k'][0] == result['k'][1]:
        k = 'Прямая'
    else:
        k = 'Вниз'

    if result['d'][0] > result['d'][1]:
        d = 'Вверх'
    elif result['d'][0] == result['d'][1]:
        d = 'Прямая'
    else:
        d = 'Вниз'

    return k, d


def zone(result):
    '''Определяем в какой зоне находимся'''

    k = ''
    d = ''

    if result['k'][0] in P.open(0, 20):
        k = 'Продажа'
    elif result['k'][0] in P.open(20, 50):
        k = 'Перепроданность'
    elif result['k'][0] in P.open(50, 80):
        k = 'Покупка'
    elif result['k'][0] in P.open(80, 100):
        k = 'Перепроданность'
    else:
        k = 'None'

    if result['d'][0] in P.open(0, 20):
        d = 'Продажа'
    elif result['d'][0] in P.open(20, 50):
        d = 'Перепроданность'
    elif result['d'][0] in P.open(50, 80):
        d = 'Покупка'
    elif result['d'][0] in P.open(80, 100):
        d = 'Перепроданность'
    else:
        d = 'None'

    return k, d


def line_indicator(result):
    '''Собираем сведения для формирвоания анализа линии D'''

    line_date = []
    line_turn = []
    line_price = []
    line_type = []

    for i in range(1, len(result)-1):
        if result['d'][i] in P.open(80, 100) and result['d'][i-1] < result['d'][i] > result['d'][i+1]:
            line_turn.append(result['d'][i])
            line_price.append(result['close'][i])
            line_type.append('Сопротивление')
            line_date.append(result['dates'][i])

        if result['d'][i] in P.open(0, 20) and result['d'][i-1] > result['d'][i] < result['d'][i+1]:
            line_turn.append(result['d'][i])
            line_price.append(result['close'][i])
            line_type.append('Поддержка')
            line_date.append(result['dates'][i])

    line_result = pd.DataFrame(data={
        'date': line_date,
        'turn': line_turn,
        'price': line_price,
        'type_line': line_type,
    })

    return line_result


def creating_table(ticker, timeframe):
    result = create_last_line(ticker, timeframe)
    motion_k, motion_d = motion(result)
    zone_k, zone_d = zone(result)
    line_d = line_indicator(result)

    analysis = []

    analysis.append(ticker)
    analysis.append(timeframe)
    analysis.append(result['k'][0])
    analysis.append(motion_k)
    analysis.append(zone_k)
    analysis.append(result['d'][0])
    analysis.append(motion_d)
    analysis.append(zone_d)

    return analysis, line_d


def main():
    tickers = ['BTC/USDT']
    # timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    timeframes = ['4h']

    for ticker in tickers:
        # print(colored(f'\nTicker = {ticker}', 'green', attrs=['bold']))
        for timeframe in timeframes:
            # print(colored(
                # f'\n-----------------------------------------------------', 'blue', attrs=['bold']))
            # print(colored(f'Timeframe = {timeframe}', 'blue', attrs=['bold']))
            # result = determining_the_position(ticker, timeframe)
            result = get_candels_dataframe(ticker, timeframe)
            # analysis, line_d = creating_table(ticker, timeframe)
            # print(colored(f'\nStochastic RSI', 'yellow', attrs=['bold']))
            # logger.info(f'\nlast_line\n{result}')
            # logger.info(f'\ntable\n{analysis}\nline_d\n')
            # print(line_d.iloc[0]['Цена'])
            # logger.info(f'analysis[2] = {analysis[2]}')
            # print(line_d)
            # print(f'Длина line_d = {len(line_d)}')

            # for i in range(len(line_d)):
            #     print(f'Разворот: {line_d.iloc[i][0]}')
            #     print(f'Цена: {line_d.iloc[i][1]}')
            #     print(f'Линия: {line_d.iloc[i][2]}')


if __name__ == "__main__":
    result = main()
