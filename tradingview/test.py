import numpy as np
import pandas as pd


def current_pattern(data):
    pattern = 'нет'

    if len(data) == 1 and data.head(1).position.values == 0:
        pattern = 'нулевой крест (продажа)'

    if len(data) == 1 and data.head(1).position.values == 1:
        pattern = 'нулевой крест (покупка)'

    # Checking the trend for the "Two Peaks" signal event

    # To sell, you need to find two decreasing minima
    # located above the zero mark (a sell signal), or two
    # rising maxima located below the zero mark (a buy signal).

    peaks = list()

    if len(data) > 1:
        if data.head(1).color.values == 'green':
            for index in data.index:
                print(index)
                if data.loc[index]['color'] == 'green' and data.loc[index + 1]['color'] == 'red':
                    peaks.append(data.loc[index]['ao'])
    print(f'peaks: {peaks}')
    return pattern


if __name__ == '__main__':
    data = pd.read_excel('/home/user/code/app-test/tradingview/data.xlsx')
    current_pattern(data)
   
