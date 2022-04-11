# Trading in the direction of a strong trend reduces risk
# and increases profit potential. The average directional index (ADX)
# is used to determine when the price is trending strongly. In many cases,
# it is the ultimate trend indicator. After all, the trend may be your
# friend, but it sure helps to know who your friends are. In this article,
# we'll examine the value of ADX as a trend strength indicator.

import pandas as pd
import numpy as np
from ta import trend, momentum, volatility


class ADX:
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int = 14,
        th: int = 20,
    ):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self.di_plus = None
        self._run()

    def _run(self):
        self.dm_plus = self._high - self._high.shift(1)
        self.dm_minus = self._low.shift(1) - self._low

        self.atr = volatility.AverageTrueRange(
            self._high, self._low, self._close).average_true_range()

        self.ema = trend.EMAIndicator(self._close).ema_indicator()

        self.di_plus = 100 * (trend.EMAIndicator(self.dm_plus).ema_indicator() / self.atr)
        self.di_minus = 100 * (trend.EMAIndicator(self.dm_minus).ema_indicator() / self.atr)
        print(f'self.di_plus:\n{self.di_plus}')
        print(f'self.di_minus:\n{self.di_minus}')
        # print(f'TYPE: {self.atr})')

    def atr(self):
        return self.atr

    def di_plus(self):
        return self.di_plus