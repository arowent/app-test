"""
Tools for calculating trend characteristics

color_detection() -> color detection
position_determination() -> position determination
"""
import sys
import numpy as np
import pandas as pd
import portion as P
import re


def color_detection(data: pd.Series) -> pd.Series:
    """color detection"""
    color = []
    for i in range(0, len(data)):
        try:
            if data[i - 1] > data[i]:
                color.append('red')
            else:
                color.append('green')
        except KeyError:
            color.append('green')
    return pd.Series(color)


def position_determination(data: pd.Series) -> pd.Series:
    """
    Position determination
    result["signal"] > 0 -> positional signal (1)
    result["signal"] <0 -> positional signal (0)
    """
    position = []

    for i in range(0, len(data)):
        try:
            if data[i] > 0:
                position.append(1)
            else:
                position.append(0)
        except KeyError:
            position.append(np.nan)
    return pd.Series(position)


def trend_direction(data: pd.Series) -> pd.Series:
    """
    Position direction
    result["position"] == 0 -> positional signal 'медвежий'
    result["position"] == 1 -> positional signal 'бычий'
    """
    direction = []
    for i in range(0, len(data)):
        try:
            if data[i] > 0:
                direction.append('бычий')
            else:
                direction.append('медвежий')
        except Exception as err:
            print(f'Unexpected error: {err.__str__()}')
            direction.append(np.nan)
    return pd.Series(direction)


def last_trend(data):
    """Creating a new table with the latest values of one trend direction"""
    data = data.head(len(data)-1)
    result = data.reindex(index=data.index[::-1])
    direction = result.head(1)['direction'].values[0]
    table = []

    for index in result.index:
        if result.loc[index]['direction'] == direction:
            table.append(result.loc[index])
        else:
            break
    return pd.DataFrame(table)


def trend_phase(data: pd.Series) -> pd.Series:
    """Determining the trend phase"""
    phase = []

    for index in data:
        if index == 'green':
            phase.append('покупка')
        else:
            phase.append('продажа')
    return pd.Series(phase)


def trend_bars(data):
    """Determining the number of trend bars"""
    bars = 0
    flag = data.head(1)['color'].values[0]

    for i in data.index:
        if data['color'][i] == flag:
            bars += 1
        else:
            break
    return bars


def trend_wave(data):
    """Determining the number of waves"""
    flag = data.head(1)['color'].values[0]
    flag_row = None
    row = ''

    for index in data.index:
        row += data.loc[index]['color']

    if flag == 'green':
        result = re.findall(r'greenred', row)
        flag_row = 'greenred'
    else:
        result = re.findall(r'redgreen', row)
        flag_row = 'redgreen'

    result = result.count(flag_row)

    if data.head(1)['color'].values[0] == data.tail(1)['color'].values[0]:
        result += 1

    if result == 0:
        result = 1

    return result


def trend_level(data: pd.Series) -> pd.Series:
    """Determining the level"""
    level = []

    for index in data:
        if index in P.open(0.0, 0.10):
            level.append('+0.00')
        elif index in P.open(0.1, 0.2):
            level.append('+0.10')
        elif index in P.open(0.2, 0.3):
            level.append('+0.20')
        elif index in P.open(0.3, 0.4):
            level.append('+0.30')
        elif index in P.open(0.4, 0.5):
            level.append('+0.40')
        elif index in P.open(0.5, 0.6):
            level.append('+0.50')
        elif index in P.open(0.6, 0.7):
            level.append('+0.60')
        elif index in P.open(0.7, 0.8):
            level.append('+0.70')
        elif index in P.open(-0.1, 0.0):
            level.append('-0.00')
        elif index in P.open(-0.2, -0.1):
            level.append('-0.10')
        elif index in P.open(-0.3, -0.2):
            level.append('-0.20')
        elif index in P.open(-0.4, -0.3):
            level.append('-0.30')
        elif index in P.open(-0.5, -0.4):
            level.append('-0.40')
        elif index in P.open(-0.6, -0.5):
            level.append('-0.50')
        elif index in P.open(-0.7, -0.6):
            level.append('-0.60')
        elif index in P.open(-0.8, -0.7):
            level.append('-0.70')
        elif index in P.open(-1.5, -0.8):
            level.append('-0.80')
        else:
            level.append(np.nan)

    return pd.Series(level)


class Strength:
    """
    The strength is determined by assessing the past volume of transactions,
    volatility, directions through which it is possible to make an analysis
    and determine the real intentions of buyers and sellers.
    """

    def __init__(self, series: pd.Series):
        self.data = series
        self.maxsize = sys.maxsize
        self.minsize = -sys.maxsize

    def strength_ao(self) -> pd.Series:
        """Determining trend strength for the Awesome Oscillator indicator"""
        strength = list()
        for index in self.data:
            if index in P.open(0, 2000) or index in P.open(-2000, 0):
                strength.append('слабый')
            elif index in P.open(2000, 3999) or index in P.open(-3999, -2000):
                strength.append('средний')
            elif index in P.open(4000, self.maxsize) or index in P.open(self.minsize, -4000):
                strength.append('сильный')
            else:
                strength.append('слабый')
        return pd.Series(strength)

    def strength_smiio(self) -> pd.Series:
        """Determining trend strength for the SMI Ergodic indicator"""
        strength = list()

        for index in self.data:
            if index in P.open(0, 0.2) or index in P.open(-0.2, 0):
                strength.append('слабый')
            elif index in P.open(0.2, 0.4) or index in P.open(-0.4, -0.2):
                strength.append('средний')
            elif index in P.open(0.4, 0.6) or index in P.open(-0.6, -0.4):
                strength.append('сильный')
            elif index in P.open(0.6, 1) or index in P.open(-1, -0.6):
                strength.append('максимум')
            else:
                strength.append('слабый')
        return pd.Series(strength)
