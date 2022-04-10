# Trading in the direction of a strong trend reduces risk
# and increases profit potential. The average directional index (ADX)
# is used to determine when the price is trending strongly. In many cases,
# it is the ultimate trend indicator. After all, the trend may be your
# friend, but it sure helps to know who your friends are. In this article,
# we'll examine the value of ADX as a trend strength indicator.

import pandas as pd
import numpy as np
from ta import trend, momentum


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
        self._th = th
        self._run()

    def _run(self):
        self.true_range = np.maximum(np.maximum((self._high - self._low),
                                                abs(self._high - self._close.shift(1))),
                                     abs(self._low - self._close.shift(1)))

        # self.direction_plus = np.where(
        #     (self._high - self._high.shift(1) > self._low.shift(1) - self._low),
        #     np.maximum(self._high - self._high.shift(1), 0), 0)
        #
        # self.direction_minus = np.where(
        #     (self._low.shift(1) - self._low > self._high - self._high.shift(1)),
        #     np.maximum(self._low.shift(1) - self._low, 0), 0)
        self.direction_plus = np.where(
            self._high - self._high.shift(1) > 0, self._high - self._high.shift(1), 0
        )

        self.direction_minus = np.where(
            self._low.shift(1) - self._low > 0, self._low.shift(1) - self._low, 0
        )

        self.smooth_true_range = pd.Series([0 for i in range(len(self._high))])
        self.smooth_true_range = self.smooth_true_range.shift(1).fillna(0) - (
                self.smooth_true_range.shift(1).fillna(0) / self._window) + self.true_range

        self.smooth_direction_plus = pd.Series([i == 100 for i in range(len(self._high))])
        self.smooth_direction_plus = self.smooth_direction_plus.shift(1) - (
                self.smooth_direction_plus.shift(1) / self._window) + 1

        print(f'FINISH SMOOTH:\n{self.smooth_direction_plus[90:]}')

        self.smooth_direction_minus = pd.Series([i == 0 for i in range(len(self._high))])
        self.smooth_direction_minus = self.smooth_direction_minus.shift(1) - (
                self.smooth_direction_minus.shift(1) / self._window) + self.direction_minus

        print(f'FINISH SMOOTH MINUS:\n{self.smooth_direction_minus[90:]}')

        self.di_plus = self.smooth_direction_plus / self.smooth_true_range * 100
        self.di_minus = self.smooth_direction_minus / self.smooth_true_range * 100

        # self.dx = abs((self.di_plus - self.di_minus) / (self.di_plus + self.di_minus)) * 100
        # self.adx = trend.SMAIndicator(self.dx, self._window).sma_indicator()
        # self.adx.to_excel('adx.xlsx')

        # print(self.smooth_true_range)
        # print(f'DIREC PLUS:\n{self.di_plus}')
        df_result = pd.DataFrame(data={
            'high': self._high,
            'low': self._low,
            'close': self._close,
            'true_range': self.true_range,
            'direction_plus': self.direction_plus,
            'direction_minus': self.direction_minus,
            'smooth_true_range': self.smooth_true_range,
            'smooth_direction_plus': self.smooth_direction_plus,
            'smooth_direction_minus': self.smooth_direction_minus,
            'di_plus': self.di_plus,
            'di_minus': self.di_minus,
            # 'adx': self.adx,
        })
        df_result.to_excel('ADX_RESULT.xlsx')
        # print(self.di_plus)

        # print(self.smooth_true_range)

    def adx_pos(self):
        return self.dm_plus

    def adx_neg(self):
        return self._minus_di
