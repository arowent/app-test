import sys
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
from ta import momentum, trend
import tools


def get_candles(symbol, timeframe):
    """Taking candles from binance"""
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(symbol, timeframe, limit=100)

    return result


def get_candels_dataframe(symbol, timeframe):
    candels = get_candles(symbol, timeframe)

    dates = list()
    time = list()
    open_data = list()
    high_data = list()
    low_data = list()
    close_data = list()
    volume_data = list()

    for candle in candels:
        dates.append(datetime.fromtimestamp(
            candle[0] / 1000.0).strftime('%d.%m.%Y %H:%M'))
        time.append(candle[0])
        open_data.append(candle[1])
        high_data.append(candle[2])
        low_data.append(candle[3])
        close_data.append(candle[4])
        volume_data.append(candle[5])

    result = pd.DataFrame(data={
        'dates': dates,
        'time': time,
        'open': open_data,
        'high': high_data,
        'low': low_data,
        'close': close_data,
        'volume': volume_data,
    })

    result['ao'] = momentum.AwesomeOscillatorIndicator(result['high'], result['low'], 5, 34).awesome_oscillator().round(
        4)
    result['color'] = tools.color_detection(result['ao'])
    result['position'] = tools.position_determination(result['ao'])
    result['direction'] = tools.trend_direction(result['ao'])
    result['strength'] = tools.Strength(result['ao']).strength_ao()
    result['phase'] = tools.trend_phase(result['color'])

    print(f'get_candels_dataframe | result:\n{result}')

    return result


def current_pattern(data):
    # If the length of the DataFrame is equal to 1, then an event has occurred (zero cross signal)

    # If the trend position is 0, then the previous trend position was 1.
    # The zero cross worked out and moved to another position relative to 0.
    # Similarly, if the trend position was 1.
    pattern = 'нет'

    if len(data) == 1 and data.head(1).position.values == 0:
        pattern = 'Нулевой крест (продажа)'

    if len(data) == 1 and data.head(1).position.values == 1:
        pattern = 'Нулевой крест (покупка)'

    # Checking the trend for the "Two Peaks" signal event

    # To sell, you need to find two decreasing minima
    # located above the zero mark (a sell signal), or two
    # rising maxima located below the zero mark (a buy signal).
    peaks = list()
    line = list()
    flag_start = data.head(1).index.values[0]
    flag_stop = data.tail(1).index.values[0]

    if len(data) > 1:
        if data.head(1).position.values == 1:
            for index in data.index:
                if index == flag_stop:
                    break
                if data['color'][index] == 'red' and data['color'][index - 1] == 'green':
                    peaks.append(data['ao'][index])

            if len(peaks) > 2 and peaks[0] < peaks[1]:
                pattern = 'Два пика (продажа)'

        if data.head(1).position.values == 0:
            for index in data.index:
                if index == flag_stop:
                    break
                if data['color'][index] == 'green' and data['color'][index - 1] == 'red':
                    peaks.append(data['ao'][index])

            if len(peaks) > 2 and peaks[0] > peaks[1]:
                pattern = 'Два пика (покупка)'

    # Checking the trend for the "Saucer" signal event

    # The "Saucer" signal is a signal about the continuation of the current trend for at
    # least one more protrusion /depression. It is formed on three (at least!)
    # consecutive columns of the AO histogram, which are a bridge
    # between two adjacent protrusions /depressions.

    if len(data) > 1:
        if data.head(1).position.values == 0:
            for index in data.index:
                if index == flag_start:
                    continue

                if index == flag_stop:
                    break

                if data['color'][index + 1] == 'red' and data['color'][index] == 'green' and data['color'][
                        index - 1] == 'green':
                    line.append(data['ao'][index + 1])
                    line.append(data['ao'][index])
                    line.append(data['ao'][index - 1])
                    break

                if len(line) == 3 and line[0] < line[1] > line[2]:
                    pattern = 'Блюдце (покупка)'

        if data.head(1).position.values == 1:
            for index in data.index:
                if index == flag_start:
                    continue

                if index == flag_stop:
                    break

                if data['color'][index + 1] == 'green' and data['color'][index] == 'red' and data['color'][
                        index - 1] == 'red':
                    line.append(data['ao'][index + 1])
                    line.append(data['ao'][index])
                    line.append(data['ao'][index - 1])
                    break

            if len(line) == 3 and line[0] > line[1] < line[2]:
                pattern = 'Блюдце (покупка)'

    return pattern


def table(symbol, timeframe):
    result = tools.last_trend(get_candels_dataframe(symbol, timeframe))
    print(f'\ntable | result:\n{result}')
    table = list()

    ao = result.head(1).ao.values[0]
    direction = result.head(1).direction.values[0]
    strength = result.head(1).strength.values[0]
    phase = result.head(1).phase.values[0]
    bars = tools.trend_bars(result)
    waves = tools.trend_wave(result)
    pattern = current_pattern(result)
    time = result.head(1).time.values[0]

    table.append(ao)
    table.append(direction)
    table.append(strength)
    table.append(waves)
    table.append(phase)
    table.append(bars)
    table.append(pattern)
    table.append(time)

    return table


def main():
    symbols = ['BTC/USDT']
    timeframes = ['15m', '1h', '4h', '1d']

    for symbol in symbols:
        for timeframe in timeframes:
            print(f'\nsymbol: {symbol} | timeframe: {timeframe}\n')
            result = table(symbol, timeframe)
            print(result)


if __name__ == '__main__':
    main()
