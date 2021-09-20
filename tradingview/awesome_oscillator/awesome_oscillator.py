import sys
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
import ta.momentum
from termcolor import colored
from ta import momentum, trend

def get_candels_dataframe(time_frame, ticker):
    result = pd.read_excel('dataframe.xlsx')
    return result

# ОПРЕДЕЛЕНИЕ ЦВЕТА

def color_detection(time_frame, ticker):
    result = get_candels_dataframe(time_frame, ticker)
    color_ao = []
    color_ao.append(2)
    for i in range(1, len(result)):
        if result['ao'][i - 1] > result['ao'][i]:
            color_ao.append('red')
        else:
            color_ao.append('green')

    result['color'] = pd.DataFrame(color_ao)
    print(f'COLOR DETECTION\n{result}')

    return result


# РАСЧЕТ ПЕРИОДА И СИГНАЛА

def implement_ao_crossover(price, ao):
    buy_price = []
    sell_price = []
    ao_signal = []
    signal = 0

    for i in range(len(ao)):
        if ao[i] > 0 and ao[i - 1] < 0:
            if signal != 1:
                buy_price.append(price[i])
                sell_price.append(np.nan)
                signal = 1
                ao_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ao_signal.append(0)
        elif ao[i] < 0 and ao[i - 1] > 0:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(price[i])
                signal = -1
                ao_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ao_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            ao_signal.append(0)

    return buy_price, sell_price, ao_signal


# РАСЧЕТ ПОЗИЦИИ

def determining_the_position(time_frame, ticker):
    result = color_detection(time_frame, ticker)
    buy, sell, signal = implement_ao_crossover(result['close'], result['ao'])

    position = []
    for i in range(len(signal)):
        if signal[i] > 1:
            position.append(0)
        else:
            position.append(1)

    for i in range(len(result['close'])):
        if signal[i] == 1:
            position[i] = 1
        elif signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i - 1]

    ao = result['ao']
    close_price = result['close']
    result['signal'] = pd.DataFrame(signal)
    result['position'] = pd.DataFrame(position)

    print(f'determining_the_position\n{result}')

    return result


# СОЗДАЕМ СПИСОК ИЗ ПОСЛЕДНИЙ ЗНАЧЕНИЙ

def create_last_trend(time_frame, ticker):
    result = determining_the_position(time_frame, ticker)
    """Создаем новый тренд из элементов последней позиции выше/ниже 0"""
    trend_ao = []
    trend_color = []
    trend_signal = []
    trend_position = []

    start = result['position'][len(result) - 2]

    for i in range(len(result) - 2, 0, -1):
        if result['position'][i] == start:
            trend_ao.append(result['ao'][i])
            trend_color.append(result['color'][i])
            trend_signal.append(result['signal'][i])
            trend_position.append(result['position'][i])
        else:
            flag = result['position'][i]
            break

    last_trend = pd.DataFrame(data={
        'ao': trend_ao,
        'color': trend_color,
        'signal': trend_signal,
        'position': trend_position
    })

    print(f'LAST TREND\n{last_trend}')
    last_trend.to_excel('last_trend.xlsx')
    return last_trend


# АНАЛИЗ ТРЕНДА

def trend_direction(time_frame, ticker):
    '''Определение позиции тренда'''
    last_trend = create_last_trend(time_frame, ticker)

    if last_trend['position'][0] == 0:
        return 'медвежий'
    else:
        return 'бычий'


def trend_strength(time_frame, ticker):
    '''Определение СИЛЫ тренда'''
    last_trend = create_last_trend(time_frame, ticker)
    rang = 'слабый'

    try:
        if len(last_trend) > 0:
            max_strength = min(last_trend['ao'], default=0)
            if max_strength in P.open(0, 2000) or max_strength in P.open(-2000, 0):
                rang = 'слабый'
            elif max_strength in P.open(2000, 3999) or max_strength in P.open(-3999, -2000):
                rang = 'средний'
            elif max_strength in P.open(4000, sys.maxsize) or max_strength in P.open(-sys.maxsize, -4000):
                rang = 'сильный'
            else:
                rang = 'None'
        return rang

    except Exception as err:
        return rang


def wave_count(time_frame, ticker):
    '''Определение количества ВОЛН'''
    last_trend = create_last_trend(time_frame, ticker)
    color = []
    output_list = []
    j = 0

    try:
        if len(last_trend) > 0:
            for i in last_trend['color']:
                color.append(i)
            for el in color:
                if output_list == []:
                    output_list.append(el)
                else:
                    if el != output_list[j]:
                        output_list.append(el)
                        j += 1
            if last_trend['position'][0] == 1:
                return output_list.count('green')
            else:
                return output_list.count('red')
    except Exception as err:
        return j


def trend_phase(time_frame, ticker):
    '''Определение ФАЗЫ тренда'''
    last_trend = create_last_trend(time_frame, ticker)
    phase = ''

    if last_trend['color'][0] == 'red':
        phase = 'продажа'
    else:
        phase = 'покупка'

    return phase


def bars_count(time_frame, ticker):
    '''Определение количества БАР тренда'''
    last_trend = create_last_trend(time_frame, ticker)
    bars = 0

    for i in range(0, len(last_trend)):
        if last_trend['color'][i] == last_trend['color'][0]:
            bars += 1
        else:
            break

    return bars


def current_pattern(time_frame, ticker):
    last_trend = create_last_trend(time_frame, ticker)
    pattern = []

    try:
        if len(last_trend) > 1:
            # два пика
            piks = []
            pick = {}

            for i in range(1, len(last_trend) - 1):
                if last_trend['position'][0] == 1:
                    if last_trend['color'][i] == 'red' and last_trend['color'][i + 1] == 'green':
                        pick[i] = last_trend['ao'][i]
                        piks.append(pick.copy())
                        pick.clear()
                else:
                    if last_trend['color'][i] == 'green' and last_trend['color'][i + 1] == 'red':
                        pick[i] = last_trend['ao'][i]
                        piks.append(pick.copy())
                        pick.clear()

            if len(piks) > 1:
                pick1 = list(piks[0].values())[0]
                pick2 = list(piks[1].values())[0]
                if pick2 <= 0 and pick1 <= 0 and pick2 < pick1:
                    pattern = 'Два пика (покупка)'
                elif pick2 > 0 and pick1 > 0 and pick2 > pick1:
                    pattern = 'Два пика (продажа)'
                else:
                    pattern = 'нет'
            else:
                pattern = 'нет'

            # блюдце
            dist = 0
            for i in range(1, len(last_trend) - 1):
                if last_trend['position'][0] == 1:
                    if last_trend['ao'][i - 1] > last_trend['ao'][i] < last_trend['ao'][i + 1]:
                        if 'нет' in pattern:
                            pattern = 'Блюдце (покупка)'
                            dist = i
                else:
                    if last_trend['ao'][i - 1] < last_trend['ao'][i] > last_trend['ao'][i + 1]:
                        if 'нет' in pattern:
                            pattern = 'Блюдце (продажа)'
                            dist = i
            com = 0
            for i in range(0, dist):
                com += 1
                print(last_trend['ao'][i])
            if com > 3:
                pattern = 'нет'
            print(f'Некоторое количество бар после сигнала "Блюдце". Количество = {com}')

        return pattern
    except Exception as err:
        print(f'Error line = {err}')
        return pattern


def trend_analysis(time_frame, ticker, indicator):
    result = create_last_trend(time_frame, ticker)
    trend = []
    cross = []

    if len(result) <= 1:
        if result['signal'][0] == 1:
            cross = [ticker, time_frame, indicator, 'бычий', 'слабый', 1, 'покупка', 1, 'нулевой крест (покупка)']
        elif result['signal'][0] == -1:
            cross = [ticker, time_frame, indicator, 'медвежий', 'слабый', 1, 'продажа', 1, 'нулевой крест (продажа)']
    else:
        position = trend_direction(time_frame, ticker)
        strength = trend_strength(time_frame, ticker)
        phase = trend_phase(time_frame, ticker)
        wave = wave_count(time_frame, ticker)
        bars = bars_count(time_frame, ticker)
        pattern = current_pattern(time_frame, ticker)

        trend.append(ticker)
        trend.append(time_frame)
        trend.append(indicator)
        trend.append(position)
        trend.append(strength)
        trend.append(wave)
        trend.append(phase)
        trend.append(bars)
        trend.append(pattern)

    if 'нулевой крест (покупка)' in cross or 'нулевой крест (продажа)' in cross:
        return cross
    else:
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
            trend = trend_analysis(timeframe, ticker, 'BTC/USDT')
            print(trend)


if __name__ == "__main__":
    result = main()