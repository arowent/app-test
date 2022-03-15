import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
from ta import momentum, trend

WINDOWS = [15, 30, 50, 75, 100, 120, 150, 180, 200]


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
        result[f'{window}'] = trend.sma_indicator(result['close'], window, fillna=True)

    return result


def set_points(data):
    numbers = [data[index].item() for index in data.loc[:, '15':'200']]
    points_one = list()
    points_second = list()

    # solution for the first table
    for index in range(len(numbers)):
        if numbers[index] > numbers[0]:
            points_one.append(1)
        elif numbers[index] == numbers[0]:
            points_one.append(0)
        else:
            points_one.append(-1)

    # solution for the second table
    for index in range(len(numbers)):
        if numbers[index] > data['close']:
            points_second.append(1)
        elif numbers[index] == numbers[0]:
            points_second.append(0)
        else:
            points_second.append(-1)
    print('Сумма всех баллов = {}'.format(sum(points_second)))
    result = {'one': points_one}
    print(result)
    return result


def main():
    symbol = 'BTC/USDT'
    timeframe = '1h'

    candles = get_candles(symbol, timeframe)
    print(get_candels_dataframe(candles).tail(10))
    data = get_candels_dataframe(candles)
    result = set_points(data.tail(1).loc[:, 'close':'200'])


if __name__ == '__main__':
    main()
