import os
import argparse
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
from ta import trend, momentum

BASE_DIR = Path(__file__).resolve().parent


def get_dataframe_path(timeframe):
    path = Path(BASE_DIR, 'btc-usd', 'BTC-USD_{}.csv'.format(timeframe))
    data = pd.read_csv(path).drop('timestamp', axis=1)
    return data


def main(argv):
    if argv.timeframe is not None:
        df_candles = get_dataframe_path(argv.timeframe)
        df_candles['ao'] = momentum.AwesomeOscillatorIndicator(df_candles['high'], df_candles['low'], 5, 34).awesome_oscillator()
        print(df_candles.tail(5))
    else:
        print('Please enter \'timeframe\'.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='List of arguments passed to execute the program.')
    parser.add_argument('-t', '--timeframe',
                        help='specify a \'timeframe\', например: [15m, 1h, 1d, 1w]')
    argv = parser.parse_args()
    main(argv)
