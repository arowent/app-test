import sys
import ccxt
import logging
from datetime import datetime
import pandas as pd
import numpy as np
from ta import momentum, trend
import tools


def get_candels(ticker, timeframe):
    binance = ccxt.bybit()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=40)

    return result


def RSI_Indicator(close, window=14):
    """Calculation of RSI for candles"""
    rsi = momentum.RSIIndicator(close, window, fillna=True).rsi()
    return rsi


def stochastic(data, window=14, k_window=3, d_window=3):
    """Calculation of STOCH RSI indicators"""
    min_val = data.rolling(window=window, center=False).min()
    max_val = data.rolling(window=window, center=False).max()

    stoch = ((data - min_val) / (max_val - min_val)) * 100

    K = stoch.rolling(window=k_window, center=False).mean()
    D = K.rolling(window=d_window, center=False).mean()

    return round(K, 6), round(D, 6)


def get_candels_dataframe(candels):
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
        # 'open': open_data,
        'high': high_data,
        'low': low_data,
        'close': close_data,
        # 'volume': volume_data,
    })

    result['ao'] = momentum.AwesomeOscillatorIndicator(result['high'], result['low'], 5, 34).awesome_oscillator().round(
        4)
    result['position'] = tools.position_determination(result['ao'])
    result['direction'] = tools.trend_direction(result['ao'])
    result['rsi'] = RSI_Indicator(result['close'], 14)
    result['k'], result['d'] = stochastic(result['rsi'])
    result['motion_k'] = motion(result['k'])
    result['motion_d'] = motion(result['d'])
    result['zone_k'] = zone(result['k'])
    result['zone_d'] = zone(result['d'])
    result['line'] = type_line(result['d'])
    result.to_excel('results.xlsx')

    return result


def motion(data: pd.Series) -> pd.Series:
    """We determine the direction of upward movement/Down or Straight"""
    motion = list()

    for index in range(0, len(data)):
        try:
            if data[index] > data[index - 1]:
                motion.append('Вверх')
            elif data[index] < data[index - 1]:
                motion.append('Вниз')
            else:
                motion.append('Прямая')
        except KeyError:
            motion.append(np.nan)

    return pd.Series(motion)


def zone(data: pd.Series) -> pd.Series:
    """We determine which zone we are in"""
    zone = list()

    for index in data:
        if 0 <= index <= 20:
            zone.append('Перепроданность')
        elif 20 < index <= 50:
            zone.append('Продажа')
        elif 50 < index <= 80:
            zone.append('Покупка')
        elif 80 < index <= 100:
            zone.append('Перекупленность')
        else:
            zone.append(np.nan)

    return pd.Series(zone)


def type_line(data: pd.Series) -> pd.Series:
    """We determine which zone we are in"""
    line = list()

    for index in data:
        if 0 <= index <= 20:
            line.append('Поддержка')
        elif 80 <= index <= 100:
            line.append('Сопротивление')
        else:
            line.append('нет')

    return pd.Series(line)


def line_indicator(data):
    """We collect information to form the analysis of line D"""
    df_res = data[data['line'] == 'Сопротивление']
    df_sup = data[data['line'] == 'Поддержка']

    flag_value = data.head(1)['close'].item()
    result_res = df_res['close'].to_list()
    result_sup = df_sup['close'].to_list()

    result_sum_res = list()
    result_sum_sup = list()

    while True:
        res = min(list(filter(lambda x: x > flag_value, result_res)))
        sup = max(list(filter(lambda x: x < flag_value, result_sup)))
        # result_sum_res.append(res) and result_res.remove(res)
        # result_sum_sup.append(sup) and result_sup.remove(sup)
        result_sum_res.append(res)
        result_sum_sup.append(sup)
        result_res.remove(res)
        result_sup.remove(sup)

        if len(result_sum_res) == 3 and len(result_sum_sup) == 3:
            break

    result_all = result_sum_res + result_sum_sup
    row_res = df_res[data['close'].isin(result_sum_res)]
    row_sup = df_sup[data['close'].isin(result_sum_sup)]
    new_df = pd.concat([row_res, row_sup], ignore_index=True)

    return new_df


def table(symbol, timeframe, exchange):
    candles = get_candels_dataframe(symbol, timeframe, exchange)
    result = tools.last_trend(candles)
    line = line_indicator(candles.reindex(index=candles.index[::-1]))

    if len(line) > 6:
        line = line.head(6)

    table = result.head(1)

    return table, line


def get_stochastic_oscillator(exchange: object):
    symbols = ['BTC/USDT']
    timeframes = ['1h']

    for symbol in symbols:
        for timeframe in timeframes:
            candles = get_candels(symbol, timeframe)

    return 'success'


def main():
    tickers = ['BTC/USDT']
    # timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    timeframes = ['4h']

    for ticker in tickers:
        for timeframe in timeframes:
            pass


if __name__ == "__main__":
    main()
