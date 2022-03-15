import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
from termcolor import colored
from ta import momentum, trend
import time


def get_candels(ticker, timeframe):
    """Забираем свечи с binance"""

    binance = ccxt.bybit()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=50)

    return result


def calculation_ema(close, window=5):
    """
    Формирование EMA
    и добавление нового столбца в DataFrame Pandas ["ema"]
    """

    ema_object = trend.EMAIndicator(close, window)
    ema = ema_object.ema_indicator()

    return ema.round(4)


def calculation_tsi(close, longlen=20, shortlen=5):
    """
    Формирование Stochastic Oscillator и его сигнала
    добавление нового столбца в DataFrame Pandas ["tsi"]
    """

    tsi_object = momentum.tsi(
        close, window_slow=longlen, window_fast=shortlen) / 100

    return tsi_object.round(4)


def calculation_signal(tsi, ema):
    """Формирование сигнала гистограммы"""

    signal = tsi - ema

    return signal.round(4)


def get_candels_dataframe(ticker, timeframe):
    """Формирование полученных свечей в DataFrame"""

    candles = get_candels(ticker, timeframe)

    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    # volume_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(
            candle[0] / 1000.0).strftime('%d.%m.%Y %H:%M'))
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
    result['ao'] = np.round(momentum.AwesomeOscillatorIndicator(result['high'], result['low'], 5, 34).awesome_oscillator().round(
        4), 4)
    # result['smiio (k)'] = calculation_tsi(result['close'])
    result['K%'] = np.round(momentum.TSIIndicator(result['close'], 20, 5).tsi() / 100, 4)
    result['D%'] = np.round(calculation_ema(result['K%']), 4)
    result['Osc'] = np.round(calculation_signal(result['K%'], result['D%']), 4)
    # result['color'] = color_detection(result['close'])
    # result['position'] = determining_the_position(result['smiio (o)'])

    return result


def color_detection(data):
    """
    Определение цвета бара
    бар выше предыдущего -> green
    бар ниже предыдущего -> red
    """

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
    print(f'\ncreate_last_trend() | start: {start}, flag: {flag}\n')
    print(f'\ncreate_last_trend() | data:\n{len(data)}\n')

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

    # last_trend.to_excel('last_trend.xlsx')

    return last_trend


# Анализ тренда
# направление гистограммы
# - определить силу тренда, а именно в каком силовом диапазоне
#   находится последняя закрытая свеча
# - подсчитать количество волн на протяжении тренда
# - определить в какой фазе находится последняя закрытая свеча
# - количество бар в последней фазе

def trend_direction(data):
    """определение позиции"""

    if data['position'][0] == 0:
        return 'медвежий'
    else:
        return 'бычий'


def trend_strength(data):
    """определение силы тренда"""

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
    """Определение фазы тренда"""

    if data['position'][0] == 0:
        return 'продажа'
    else:
        return 'покупка'


def trend_wave(data):
    """Определение количества ВОЛН"""

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


def trend_bars(data):
    """Определение количества БАР тренда"""
    bars = 0

    for i in range(0, len(data)):
        if data['color'][i] == data['color'][0]:
            bars += 1
        else:
            break

    return bars


def previous_bars(data, index):
    line = []

    line.append(data["tsi"][index - 1])
    line.append(data["ema"][index - 1])
    line.append(data["signal"][index - 1])
    line.append(data["tsi"][index])
    line.append(data["ema"][index])
    line.append(data["signal"][index])

    return line


def get_movement(value):
    """Определение движения линии"""
    print(f'get_movement(): {value}')
    line = []

    if value[0] > value[3]:
        line.append("Вниз")
        line.append("NO SHORTS")
    else:
        line.append("Вверх")
        line.append("NO LONGS")

    return line


def get_level(data):
    """Определение уровня"""
    level = '0.00'
    print(f'\ndata["tsi"][0]: {data["tsi"][0]}\n')
    data = data['tsi'][0]

    try:
        if data > 0:
            if data in P.open(0, 0.20):
                level = '+0.20'
            elif data in P.open(0.20, 0.40):
                level = '+0.20'
            elif data in P.open(0.20, 0.60):
                level = '+0.60'
            elif data in P.open(0.60, 1):
                level = '+0.60'
        else:
            if data in P.open(-0.20, 0):
                level = '-0.20'
            elif data in P.open(-0.40, -0.20):
                level = '-0.20'
            elif data in P.open(-0.60, -0.40):
                level = '-0.40'
            elif data in P.open(-1, -0.60):
                level = '-0.60'

        return level

    except Exception as err:
        return level


def create_table(ticker, timeframe):
    '''Формирование таблицы'''
    result = get_candels_dataframe(ticker, timeframe)
    last_trend = create_last_trend(result)
    print(f'create_table() | result:\n{result}')
    print(f'\ncreate_table() | last_trend:\n\n{last_trend}\n')
    position = trend_direction(last_trend)
    strength = trend_strength(last_trend)
    phase = trend_phase(last_trend)
    wave = trend_wave(last_trend)
    bars = trend_bars(last_trend)
    previous = previous_bars(result.tail(2), len(result) - 1)
    movement = get_movement(previous)
    print(f'last_trend.head(1):\n {last_trend.head(1)}')
    level = get_level(last_trend.head(1))

    table = []
    table.append(ticker)
    table.append(timeframe)
    table.append(position)
    table.append(strength)
    table.append(wave)
    table.append(phase)
    table.append(bars)
    table = table + previous
    table.append(movement[0])
    table.append(movement[1])
    table.append(level)

    return table


def main():
    """Главный метод вызывающий остальные"""

    start_pivot = time.perf_counter()
    tickers = ['BTC/USDT']
    # timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    timeframes = ['1h']

    for ticker in tickers:
        print(colored(f'\nticker = {ticker}', 'green', attrs=['bold']))
        for timeframe in timeframes:
            print(colored(
                f'-----------------------------------------------------', 'blue', attrs=['bold']))
            print(colored(f'timeframe = {timeframe}', 'blue', attrs=['bold']))
            trend = get_candels_dataframe(ticker, timeframe)
            print(trend.tail(8).loc[:, ['dates', 'close',
                  'ao', 'K%', 'D%', 'Osc']])
            # table = create_table(ticker, timeframe)
            # print(f'Output of the all values from "trend":\n\n{trend}')
            # print(f'\ncreate_table:\n\n{table}')S
            # print(colored(f'\ncreate_table: {table}', 'yellow', attrs=['bold']))

    print(f'\n[FINISH] main(): {time.perf_counter() - start_pivot}\n')


if __name__ == "__main__":
    main()
