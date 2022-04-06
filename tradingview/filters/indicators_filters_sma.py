import ccxt
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from ta import momentum, trend
import pprint

# Configure logging
logging.basicConfig(level=logging.INFO)

WINDOWS = [15, 30, 50, 75, 100, 120, 150, 180, 200]


# WINDOWS = [10]


def get_candles(symbol, timeframe):
    """Taking candles from binance"""
    binance = ccxt.bybit()
    result = binance.fetch_ohlcv(symbol, timeframe, limit=200)

    return result


def get_candels_dataframe(candels):
    dates = list()
    close_data = list()

    for candle in candels:
        dates.append(datetime.fromtimestamp(
            candle[0] / 1000.0).strftime('%d.%m.%Y %H:%M'))
        close_data.append(candle[4])

    result = pd.DataFrame(data={
        'dates': dates,
        'close': close_data,
    })

    for window in WINDOWS:
        result[f'{window}'] = trend.ema_indicator(result['close'], window, fillna=True)

    return result


def get_first_table(data: pd.DataFrame) -> list:
    """Solution for the first table"""
    numbers = [data[index].item() for index in data.loc[:, '15':'200']]
    columns = data.columns.tolist()[2:]
    points_one = list()

    for index in range(len(numbers)):
        if numbers[index] > numbers[0]:
            points_one.append({f'{columns[index]}': 1})
        elif numbers[index] == numbers[0]:
            points_one.append({f'{columns[index]}': 0})
        else:
            points_one.append({f'{columns[index]}': -1})
    return points_one


def get_second_table(data: pd.DataFrame) -> list:
    """Solution for the second table"""
    numbers = [data[index].item() for index in data.loc[:, '15':'200']]
    columns = data.columns.tolist()[2:]
    points_second = list()

    for index in range(len(numbers)):
        if numbers[index] > data['close'].item():
            points_second.append({f'{columns[index]}': -1})
        elif numbers[index] == data['close'].item():
            points_second.append({f'{columns[index]}': 0})
        else:
            points_second.append({f'{columns[index]}': 1})
    return points_second


def get_third_table(data: pd.DataFrame) -> list:
    """Solution for the third table"""
    row_previous = [data.head(1)[index].item() for index in data.head(1).loc[:, '15':'200']]
    row_current = [data.tail(1)[index].item() for index in data.tail(1).loc[:, '15':'200']]
    columns = data.columns.tolist()[2:]
    points_third = list()
    sma = list()

    if len(row_previous) == len(row_current):
        for i in range(len(row_current)):
            if row_current[i] > row_previous[i]:
                points_third.append({f'{columns[i]}': 1})
                sma.append({f'{columns[i]}': [np.round(row_current[i], 4), np.round(row_previous[i], 4)]})
            elif row_current[i] == row_previous[i]:
                points_third.append({f'{columns[i]}': 0})
                sma.append({f'{columns[i]}': [np.round(row_current[i], 4), np.round(row_previous[i], 4)]})
            else:
                points_third.append({f'{columns[i]}': -1})
                sma.append({f'{columns[i]}': [np.round(row_current[i], 4), np.round(row_previous[i], 4)]})
    return points_third, sma


def main():
    symbol = 'BTC/USDT'
    timeframe = '1h'

    candles = get_candles(symbol, timeframe)
    print(get_candels_dataframe(candles).tail(5))
    data = get_candels_dataframe(candles)
    points_first = get_first_table(data.tail(1))
    points_second = get_second_table(data.tail(1))
    points_third, sma = get_third_table(data.tail(2))
    # print('\n[1T]: {} | Сумма: {}'.format(points_first, sum(points_first)))
    # print('[2T]: {} | Сумма: {}'.format(points_second, sum(points_second)))
    # print('[3T]: {} | Сумма: {}'.format(points_third, sum(points_third)))
    result = dict([('sma15', points_first), ('price', points_second), ('moving', points_third)])
    pprint.pprint(result)
    print(sma)
    load(result, sma)

    # for i in result.keys():
    #     print(result[i])


def load(result, sma):
    for i in result.get('sma15'):
        print(len(result.get('sma15')))
        print(i)


if __name__ == '__main__':
    main()
