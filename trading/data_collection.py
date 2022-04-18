from matplotlib.pyplot import axis
import pandas as pd
import os
import numpy as np
from pandas.core.indexes.base import Index
from ta import momentum
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PATH = r'C:\Users\ollko\Desktop\EmEl\btc-usd'
PATHS = {
    '5m': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_5m.csv',
    '15m': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_15m.csv',
    '30m': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_30m.csv',
    '1h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_1h.csv',
    '4h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_4h.csv',
    '6h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_6h.csv',
    '12h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_12h.csv',
    '1d': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_1d.csv'
}
PATHS_ALL = {
    '5m': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_5m.csv',
    '15m': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_15m.csv',
    '30m': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_30m.csv',
    '1h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_1h.csv',
    '3h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_3h.csv',
    '4h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_4h.csv',
    '6h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_6h.csv',
    '12h': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_12h.csv',
    '1d': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_1d.csv',
    '4d': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_4d.csv',
    '1w': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_1w.csv',
    '2w': r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_2w.csv'
}
final_path = {
    '5m': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_5m.csv',
    '15m': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_15m.csv',
    '30m': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_30m.csv',
    '1h': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_1h.csv',
    '3h': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_3h.csv',
    '4h': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_4h.csv',
    '6h': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_6h.csv',
    '12h': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_12h.csv',
    '1d': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_1d.csv',
    '4d': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_4d.csv',
    '1w': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_1w.csv',
    '2w': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_2w.csv'
}


def add_missing_tf():
    ohlc_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }

    for tf in PATHS:
        df = pd.read_csv(PATHS[tf], index_col=0)
        df['timestamp'] = pd.to_datetime(df['date'])
        df.set_index('timestamp', inplace=True)
        df.to_csv(PATHS[tf])
        if tf == '1h':
            df = df.resample('3H').agg(ohlc_dict)
            df.to_csv(
                r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_3h.csv')
        elif tf == '1d':
            df = df.resample('7D').agg(ohlc_dict)
            df.to_csv(
                r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_1w.csv')
            df = df.resample('14D').agg(ohlc_dict)
            df.to_csv(
                r'/home/arowent/code/app-test/trading/btc-usd/BTC-USD_2w.csv')


def convert_to_excel():

    test_data = {
        '1w': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_1w.csv',
        '2w': r'/home/arowent/code/app-test/trading/btc-usd/transformed/BTC-USD_added_2w.csv'
    }
    writer = pd.ExcelWriter('BTC-USD_sagnal_names.xlsx', engine='xlsxwriter')
    for tf in final_path:
        df = pd.read_csv(final_path[tf])
        df = add_signals(df)
        df = df[['timestamp', 'open', 'close', 'signal', 'signal_name']]
        df = df.rename(columns={'timestamp': 'datetime'})
        df.to_excel(writer, sheet_name=tf, index=None, header=True)
    writer.save()


def add_features(time_frame):
    """function adds features needed for extracting trading signal"""

    data = pd.read_csv(PATHS_ALL[time_frame])
    data['ao'] = momentum.awesome_oscillator(high=data['high'], low=data['low'],
                                             window1=5, window2=34, fillna=False)

    def coloring(x):
        if x > 0:
            return 'red'
        elif x <= 0:
            return 'green'
        else:
            return x

    def digi_coloring(x):
        if x > 0:
            return 1
        elif x <= 0:
            return 0
        else:
            return x
    data['color'] = data['ao'].shift(1) - data['ao']
    data['digi_color'] = data['color'].apply(digi_coloring)
    data['color'] = data['color'].apply(coloring)

    # features for zero-cross signal
    data['ao_lag_1'] = data['ao'].shift(1)
    data['ao_lag_2'] = data['ao'].shift(2)
    data['ao_lag_3'] = data['ao'].shift(3)
    data['color_lag_1'] = data['color'].shift(1)
    data['color_lag_2'] = data['color'].shift(2)
    data['color_lag_3'] = data['color'].shift(3)
    data['zero_cross_signal'] = 0

    # features for bludce: same as above
    data['bludce_signal'] = 0
    data['signal'] = 0

    # features for two peaks
    data['list_colors'] = [[np.nan] if x == 0 else data['color'].iloc[np.max(
        [0, x - 100]): x - 2].tolist() for x in range(len(data))]
    data['digi_list'] = [[np.nan] if x == 0 else data['digi_color'].iloc[np.max(
        [0, x - 100]): x - 1].tolist() for x in range(len(data))]

    def reverse_fill_nan(x):
        x = x[::-1]
        while len(x) < 100:
            x.append(np.nan)
        result = x[0:100]
        return list(result)
    data['list_colors'] = data['list_colors'].apply(reverse_fill_nan)
    data['digi_list'] = data['digi_list'].apply(reverse_fill_nan)

    data['list_ao'] = [[np.nan] if x == 0 else data['ao'].iloc[np.max(
        [0, x - 100]): x - 2].tolist() for x in range(len(data))]
    data['list_ao'] = data['list_ao'].apply(reverse_fill_nan)

    data['peaks_signal'] = 0

    folder = r'/home/arowent/code/app-test/trading/btc-usd/transformed'
    name = f'BTC-USD_added_{time_frame}.csv'
    data.to_csv(os.path.join(folder, name))


def add_signals(data):

    # zero-cross signal
    def zero_cross(x):
        if ((x[0] == x[1] == x[2] == 'red')
                and (x[3] < 0 and x[4] < 0 and x[5] >= 0)):
            return -1
        elif (x[0] == x[1] == x[2] == 'green'
              and (x[3] > 0 and x[4] > 0 and x[5] <= 0)):
            return 1
        else:
            return 0

    # bludce signal
    def bludce(x):
        if x[0] == 'red' and x[1] == x[2] == 'green':
            return -1
        elif x[0] == 'green' and x[1] == x[2] == 'red':
            return 1
        else:
            return 0

    def two_peaks(x):

        def verify():
            # return True
            colors_array = x[4][1:-1].split(',')
            ao_array = x[5][1:-1].split(',')

            first_ao = ao_array[0]
            first_color = colors_array[0]
            flag = False

            for i in range(1, len(ao_array)):

                if float(ao_array[i]) * float(first_ao) < 0:
                    # print('zero crossed')
                    # print(f'first = {float(first_ao)}, compared {float(ao_array[i])} i = {i}')
                    # print(f'first color: {first_color}, comp: {colors_array[i]}')
                    # print(int(float(first_color)) == int(float(colors_array[i])))
                    # print(flag)
                    return False

                # print(float(colors_array[i]))
                # print(float(first_color))
                if not np.isnan(float(colors_array[i])) and not np.isnan(float(first_color)) and int(float(colors_array[i])) != int(float(first_color)):
                    flag = True
                if not np.isnan(float(colors_array[i])) and not np.isnan(float(first_color)) and int(float(colors_array[i])) == int(float(first_color)) and flag:
                    if np.abs(float(ao_array[i])) - np.abs(float(first_ao)) > 0:
                        return True
                    else:
                        return False

        if x[0] > 0 and x[1] == x[2] == 'red' and x[3] == 'green':
            if verify():
                return -1
            else:
                return 0

        elif x[0] < 0 and x[1] == x[2] == 'green' and x[3] == 'red':
            if verify():
                return 1
            else:
                return 0
        else:
            return 0

    def name(x):
        if x[0] != 0:
            if x[0] == 1:
                return 'Нулевой крест (покупка)'
            else:
                return 'Нулевой крест (продажа)'
        elif x[1] != 0:
            if x[1] == 1:
                return 'Блюдце (покупка)'
            else:
                return 'Блюдце (продажа)'
        elif x[2] != 0:
            if x[2] == 1:
                return 'Два пика (покупка)'
            else:
                return 'Два пика (продажа)'
        else:
            return None

    data['zero_cross_signal'] = data[['color', 'color_lag_1', 'color_lag_2',
                                      'ao', 'ao_lag_1', 'ao_lag_2']].apply(zero_cross, axis=1)

    data['bludce_signal'] = data[['color', 'color_lag_1',
                                  'color_lag_2']].apply(bludce, axis=1)
    # data['signal_name'] = data['bludce_signal'].apply(lambda x: x if x == 0 else 'Блюдце')

    data['two_peaks_signal'] = data[['ao', 'color', 'color_lag_1',
                                     'color_lag_2', 'digi_list', 'list_ao']].apply(two_peaks, axis=1)
    # data['signal_name'] = data['two_peaks_signal'].apply(lambda x: x if x == 0 else 'Два пика')
    data['signal_name'] = data[['zero_cross_signal',
                                'bludce_signal', 'two_peaks_signal']].apply(name, axis=1)
    # combine
    data['signal'] = data['two_peaks_signal'] + \
        data['zero_cross_signal'] + data['bludce_signal']
    return data


def df_replace(df):
    df_sell = df['signal_name'].replace([
        'Нулевой крест (покупка)',
        'Блюдце (покупка)',
        'Два пика (покупка)'
    ], np.nan)
    df_buy = df['signal_name'].replace([
        'Нулевой крест (продажа)',
        'Блюдце (продажа)',
        'Два пика (продажа)'
    ], np.nan)
    df = df.drop(['signal', 'signal_name'], axis=1)
    df['AO'] = momentum.awesome_oscillator(high=df['high'], low=df['low'],
                                           window1=5, window2=34, fillna=False)
    df['AO SELL'] = df_sell
    df['AO BUY'] = df_buy

    return df


def main(argv):
    if argv.timeframe is not None:
        path = Path(BASE_DIR, 'btc-usd', 'transformed',
                    'BTC-USD_added_{}.csv'.format(argv.timeframe))
        df = pd.read_csv(path)
        df = add_signals(df)
        df = df[['timestamp', 'open', 'high', 'low',
                'close', 'volume', 'signal', 'signal_name']]
        df = df_replace(df)
        df.to_csv(
            'trading/btc-usd/final/btc_usd_{}.csv'.format(argv.timeframe))
    else:
        print('Please enter \'timeframe\'.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='List of arguments passed to execute the program.')
    parser.add_argument('-t', '--timeframe',
                        help='specify a \'timeframe\', например: [15m, 1h, 1d, 1w]')
    argv = parser.parse_args()
    main(argv)
