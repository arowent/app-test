# Trading in the direction of a strong trend reduces risk
# and increases profit potential. The average directional index (ADX)
# is used to determine when the price is trending strongly. In many cases,
# it is the ultimate trend indicator. After all, the trend may be your
# friend, but it sure helps to know who your friends are. In this article,
# we'll examine the value of ADX as a trend strength indicator.

import pandas as pd
import numpy as np


class ADX:
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 14,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._run()
    
    def _run(self):
        adx_pos = self._high.diff()
        adx_neg = self._low.diff()
        # print(adx_pos)
        adx_pos[adx_pos < 0] = 0.0
        tr1 = pd.DataFrame(self._high - self._low)
        tr2 = pd.DataFrame(abs(self._high - self._close.shift(1)))
        tr3 = pd.DataFrame(abs(self._low - self._close.shift(1)))
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis=1, join='inner').max(axis=1)
        atr = tr.rolling(self._window).mean()
        self._plus_di = 100 * (adx_pos.ewm(alpha=1 / self._window).mean() / atr)
        self._minus_di = abs(100 * (adx_neg.ewm(alpha=1 / self._window).mean() / atr))

    def adx_pos(self):
        def ADX(df: pd.DataFrame(), interval: int = 14):
            df['-DM'] = df['Low'].shift(1) - df['Low']
            df['+DM'] = df['High'] - df['High'].shift(1)
            df['+DM'] = np.where((df['+DM'] > df['-DM']) & (df['+DM'] > 0), df['+DM'], 0.0)
            df['-DM'] = np.where((df['-DM'] > df['+DM']) & (df['-DM'] > 0), df['-DM'], 0.0)
            df['TR_TMP1'] = df['High'] - df['Low']
            df['TR_TMP2'] = np.abs(df['High'] - df['Adj Close'].shift(1))
            df['TR_TMP3'] = np.abs(df['Low'] - df['Adj Close'].shift(1))
            df['TR'] = df[['TR_TMP1', 'TR_TMP2', 'TR_TMP3']].max(axis=1)
            df['TR' + str(interval)] = df['TR'].rolling(interval).sum()
            df['+DMI' + str(interval)] = df['+DM'].rolling(interval).sum()
            df['-DMI' + str(interval)] = df['-DM'].rolling(interval).sum()
            df['+DI' + str(interval)] = df['+DMI' + str(interval)] / df['TR' + str(interval)] * 100
            df['-DI' + str(interval)] = df['-DMI' + str(interval)] / df['TR' + str(interval)] * 100
            df['DI' + str(interval) + '-'] = abs(df['+DI' + str(interval)] - df['-DI' + str(interval)])
            df['DI' + str(interval)] = df['+DI' + str(interval)] + df['-DI' + str(interval)]
            df['DX'] = (df['DI' + str(interval) + '-'] / df['DI' + str(interval)]) * 100
            df['ADX' + str(interval)] = df['DX'].rolling(interval).mean()
            df['ADX' + str(interval)] = df['ADX' + str(interval)].fillna(df['ADX' + str(interval)].mean())
            del df['TR_TMP1'], df['TR_TMP2'], df['TR_TMP3'], df['TR'], df['TR' + str(interval)]
            del df['+DMI' + str(interval)], df['DI' + str(interval) + '-']
            del df['DI' + str(interval)], df['-DMI' + str(interval)]
            del df['+DI' + str(interval)], df['-DI' + str(interval)]
            del df['DX']
            return df

    def adx_neg(self):
        return self._minus_di

"""
def get_adx(high, low, close, lookback):
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.rolling(lookback).mean()
    
    plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha = 1/lookback).mean()
    return plus_di, minus_di, adx_smooth

aapl['plus_di'] = pd.DataFrame(get_adx(aapl['high'], aapl['low'], aapl['close'], 14)[0]).rename(columns = {0:'plus_di'})
aapl['minus_di'] = pd.DataFrame(get_adx(aapl['high'], aapl['low'], aapl['close'], 14)[1]).rename(columns = {0:'minus_di'})
aapl['adx'] = pd.DataFrame(get_adx(aapl['high'], aapl['low'], aapl['close'], 14)[2]).rename(columns = {0:'adx'})
aapl = aapl.dropna()
aapl.tail()
"""