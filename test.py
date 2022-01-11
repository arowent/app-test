import pandas as pd
from ta import momentum
import time
import numpy as np


def color_detection(data: pd.Series) -> pd.Series:
    """color detection"""
    color = list()
    for i in range(0, len(data)):
        try:
            if data[i - 1] > data[i]:
                color.append('red')
            else:
                color.append('green')
        except KeyError:
            color.append(np.nan)
    return pd.Series(color)


def color_detection_shift(data: pd.Series) -> pd.Series:
    """color detection with shift and apply"""
    data = data.to_frame(name='ao')
    data['color'] = data['ao'].shift(1) - data['ao']
    data['color'] = data['color'].apply(lambda x: 'red' if x > 0 else 'green')
    data['color'].values[0] = np.nan
    return pd.Series(data['color'])



data = pd.read_csv(r'C:\Users\ollko\Desktop\EmEl\btc-usd\BTC-USD_5m.csv')
data['ao'] = momentum.AwesomeOscillatorIndicator(data['high'], data['low'], 5, 34).awesome_oscillator().round(4)
data = data['ao']


start_time = time.time()
result_for = color_detection(data)
print(f'Time ellapsed with for loop {time.time() - start_time}')
print(result_for.head(5))


start_time = time.time()
result_shift = color_detection_shift(data)
print(f'Time ellapsed with shift {time.time() - start_time}')
print(result_shift.head(5))


print((result_for == result_shift).value_counts())



