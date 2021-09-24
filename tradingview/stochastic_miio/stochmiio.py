import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
from termcolor import colored
from ta import momentum, trend
import time

def get_candels(ticker, timeframe):
    '''Забираем свечи с binance'''

    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=500)

    return result

def calculation_ema(close, window=5):
    '''
    Формирование EMA
    и добавление нового столбца в DataFrame Pandas ["ema"]
    '''

    ema_object = trend.EMAIndicator(close, window)
    ema = ema_object.ema_indicator()

    return ema.round(4)

def calculation_tsi(close, longlen=20, shortlen=5):
    '''
    Формирование Stochastic Oscillator и его сигнала
    добавление нового столбца в DataFrame Pandas ["tsi"]
    '''

    tsi_object = momentum.tsi(close, window_slow=longlen, window_fast=shortlen) / 100
    
    return tsi_object.round(4)

def calculation_signal(tsi, ema):
    '''Формирование сигнала гистограммы'''

    signal = tsi - ema

    return signal.round(4)

def get_candels_dataframe(ticker, timeframe):
    '''Формирование полученных свечей в DataFrame'''

    candles = get_candels(ticker, timeframe)

    dates = []
    # open_data = []
    # high_data = []
    # low_data = []
    close_data = []
    # volume_data = []

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

    result['tsi'] = calculation_tsi(result['close'])
    result['ema'] = calculation_ema(result['tsi'])
    result['signal'] = calculation_signal(result['tsi'], result['ema'])
    result['color'] = color_detection(result['close'])
    result['position'] = determining_the_position(result['signal'])

    result.to_excel('stochframe.xlsx')

    return result.head(len(result)-1)

def color_detection(data):
    '''
    Определение цвета бара
    бар выше предыдущего -> green
    бар ниже предыдущего -> red
    '''

    # print(f'color_detection():\n{data}')
    color_signal = []

    for i in range(0, len(data)):
        try:
            if data[i - 1] > data[i]:
                color_signal.append('red')
            else:
                color_signal.append('green')
        except KeyError:
            color_signal.append(np.nan)

    # print(f'\ncolor_signal():\n{color_signal}\n')

    return color_signal

def determining_the_position(data):
    '''
    Определение позиции
    result["signal"] > 0 -> position_signal (1)
    result["signal"] < 0 -> position_signal (0)
    '''
    position_signal = []

    for i in range(0, len(data)):
        try:
            if data[i] > 0:
                position_signal.append(1)
            else:
                position_signal.append(0)
        except KeyError:
            position_signal.append(np.nan)

    # print(f'\ncolor_signal():\n{color_signal}\n')

    return position_signal

def create_last_trend(data):
    """Создаем новый тренд из элементов последней позиции выше/ниже 0"""

    last_tsi = []
    last_ema = []
    last_signal = []
    last_color = []
    last_position = []

    start, flag = data['position'][len(data) - 1], data['close'][len(data) - 1]
    # print(f'\ncreate_last_trend() | start: {start}, flag: {flag}\n')

    for i in range(len(data) - 1, 0, -1):
        if data['position'][i] == start:
            last_tsi.append(data['tsi'][i])
            last_ema.append(data['ema'][i])
            last_signal.append(data['signal'][i])
            last_color.append(data['color'][i])
            last_position.append(data['position'][i])
        else:
            flag = data['position'][i]
            break

    last_trend = pd.DataFrame(data={
        'tsi': last_tsi,
        'ema': last_ema,
        'signal': last_signal,
        'color': last_color,
        'position': last_position,
    })

    last_trend.to_excel('last_trend.xlsx')

    return last_trend

# Анализ тренда
# направление гистограммы
# - определить силу тренда, а именно в каком силовом диапазоне 
#   находится последняя закрытая свеча
# - подсчитать количество волн на протяжении тренда
# - определить в какой фазе находится последняя закрытая свеча
# - количество бар в последней фазе

def trend_direction(data):
    '''определение позиции'''

    if data['position'][0] == 0:
        return 'медвежий'
    else:
        return 'бычий'

def trend_strength(data):
    '''определение силы тренда'''

    rang = 'слабый'

    try:
        if data['signal'][0] in P.open(0, 0.20) or data['signal'][0] in P.open(-0.20, 0):
            rang = 'слабый'
        elif data['signal'][0] in P.open(0.20, 0.40) or data['signal'][0] in P.open(-0.40, -0.20):
            rang = 'средний'
        elif data['signal'][0] in P.open(0.40, 0.60) or data['signal'][0] in P.open(-0.60, -0.40):
            rang = 'сильный'
        elif data['signal'][0] in P.open(0.60, 1) or data['signal'][0] in P.open(-1, -0.60):
            rang = 'максимум'
        
        return rang

    except Exception as err:
        return rang

def trend_phase(data):
    '''Определение фазы тренда'''

    if data['position'][0] == 0:
        return 'продажа'
    else:
        return 'покупка'

def trend_wave(data):
    '''Определение количества ВОЛН'''

    color = []
    output_list = []
    j = 0

    try:
        if len(data) > 0:
            for i in data['color']:
                color.append(i)
            for el in color:
                if output_list == []:
                    output_list.append(el)
                else:
                    if el != output_list[j]:
                        output_list.append(el)
                        j += 1
            if data['position'][0] == 1:
                return output_list.count('green')
            else:
                return output_list.count('red')
    except Exception as err:
        return j


def create_table(ticker, timeframe):
    result = get_candels_dataframe(ticker, timeframe)
    last_trend = create_last_trend(result)
    # print(f'create_table() | result:\n{result}')
    print(f'\ncreate_table() | last_trend:\n\n{last_trend}\n')
    position = trend_direction(last_trend)
    strength = trend_strength(last_trend)
    phase = trend_phase(last_trend)
    wave = trend_wave(last_trend)
    # bars = bars_count(time_frame, ticker)
    # pattern = current_pattern(time_frame, ticker)

    table = []
    table.append(ticker)
    table.append(timeframe)
    table.append(position)
    table.append(strength)
    table.append(phase)
    table.append(wave)

    return table


def main():
    '''Главный метод вызывающий остальные'''

    start_pivot = time.perf_counter()
    tickers = ['BTC/USDT']
    # timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    timeframes = ['15m']

    for ticker in tickers:
        print(colored(f'\nticker = {ticker}', 'green', attrs=['bold']))
        for timeframe in timeframes:
            print(colored(f'-----------------------------------------------------', 'blue', attrs=['bold']))
            print(colored(f'timeframe = {timeframe}', 'blue', attrs=['bold']))
            trend = get_candels_dataframe(ticker, timeframe)
            table = create_table(ticker, timeframe)
            # print(f'Output of the all values from "trend":\n\n{trend}')
            # print(f'\ncreate_table:\n\n{table}')
            print(colored(f'\ncreate_table: {table}', 'yellow', attrs=['bold']))

    print(f'\n[FINISH] main(): {time.perf_counter() - start_pivot}\n')


if __name__ == "__main__":
    main()