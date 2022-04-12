# Trading in the direction of a strong trend reduces risk
# and increases profit potential. The average directional index (ADX)
# is used to determine when the price is trending strongly. In many cases,
# it is the ultimate trend indicator. After all, the trend may be your
# friend, but it sure helps to know who your friends are. In this article,
# we'll examine the value of ADX as a trend strength indicator.

import logging
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
        self._dx = None
        self._di_plus = None
        self._di_minus = None
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._th = th
        self._run()

    def _run(self):
        self.true_range = np.maximum(np.maximum((self._high - self._low),
                                                abs(self._high - self._close.shift(1).fillna(0))),
                                     abs(self._low - self._close.shift(1).fillna(0)))

        self.direction_plus = np.where(
            (self._high - self._high.shift(1) > self._low.shift(1) - self._low),
            np.maximum(self._high - self._high.shift(1), 0), 0)

        self.direction_minus = np.where(
            (self._low.shift(1) - self._low > self._high - self._high.shift(1)),
            np.maximum(self._low.shift(1) - self._low, 0), 0)
        # self.direction_plus = np.where(
        #     self._high -
        #     self._high.shift(1).fillna(0) > 0, self._high -
        #     self._high.shift(1).fillna(0), 0
        # )

        # self.direction_minus = np.where(
        #     self._low.shift(1).fillna(
        #         0) - self._low > 0, self._low.shift(1).fillna(0) - self._low, 0
        # )

        self.smooth_true_range = [0]
        for i in range(1, len(self.true_range)):
            #print(f'smooth_true_range [i]: {self.smooth_true_range} true_range = {self.true_range}')
            self.smooth_true_range.append(self.smooth_true_range[i-1] - (
                self.smooth_true_range[i-1] / self._window) + self.true_range.loc[i])

        self.smooth_true_range = pd.Series(self.smooth_true_range)

        print(f'SMOOTH TRUE RANGE:\n{self.smooth_true_range}')

        # self.smooth_direction_plus = pd.Series([0 for i in range(len(self._high))])
        # self.smooth_direction_plus = self.smooth_direction_plus.shift(1).fillna(0) - (
        #     self.smooth_direction_plus.shift(1).fillna(0) / self._window) + self.direction_plus

        # smooth_direction_plus
        self.smooth_direction_plus = [0]
        for i in range(1, len(self.true_range)):
            self.smooth_direction_plus.append(self.smooth_direction_plus[i-1] - (
                self.smooth_direction_plus[i-1] / self._window) + self.direction_plus[i])
        self.smooth_direction_plus = pd.Series(self.smooth_direction_plus)

        # smooth_direction_minus
        self.smooth_direction_minus = [0]
        for i in range(1, len(self.true_range)):
            self.smooth_direction_minus.append(self.smooth_direction_minus[i-1] - (
                self.smooth_direction_minus[i-1] / self._window) + self.direction_minus[i])
        self.smooth_direction_minus = pd.Series(self.smooth_direction_minus)


        # result ADX
        self._di_plus = np.round(self.smooth_direction_plus / self.smooth_true_range * 100, 1)
        self._di_minus = np.round(self.smooth_direction_minus / self.smooth_true_range * 100, 1)

        self._dx = (abs(self._di_plus - self._di_minus) /
                       (self._di_plus + self._di_minus)) * 100
        self._adx = np.round(trend.SMAIndicator(self._dx, self._window).sma_indicator(), 1)

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
            'di_plus': self._di_plus,
            'di_minus': self._di_minus,
            'adx': self._adx,
        })
        df_result.to_excel('ADX_RESULT.xlsx')

    def adx(self):
        # self.adx = trend.SMAIndicator(self.dx, self._window).sma_indicator()
        return self._adx

    def adx_pos(self):
        # self.adx = trend.SMAIndicator(self.dx, self._window).sma_indicator()
        return self._di_plus

    def adx_neg(self):
        # self.adx = trend.SMAIndicator(self.dx, self._window).sma_indicator()
        return self._di_minus
