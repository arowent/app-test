import os
import argparse
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent


def get_dataframe_path(timeframe):
    return Path(BASE_DIR, 'btc-usd', 'BTC-USD_{}.csv'.format(timeframe))


def main(argv):
    if argv.timeframe is not None:
        df_candles = pd.read_csv(get_dataframe_path(argv.timeframe)).drop('timestamp', axis=1)
        print(df_candles.tail(5))
    else:
        print('Please enter \'timeframe\'.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='List of arguments passed to execute the program.')
    parser.add_argument('-t', '--timeframe',
                        help='specify a \'timeframe\', for example: [15m, 1h, 1d, 1w]')
    argv = parser.parse_args()
    main(argv)
