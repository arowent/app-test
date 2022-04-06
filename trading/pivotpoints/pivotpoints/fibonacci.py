import ccxt
import logging
import datetime
import pandas as pd
import numpy as np


class Fibonacci:
    """Pivot Point Fibonacci

    Fibonacci's analysis can supercharge your market performance, but you'll
    need to master a few tricks of the trade to gain maximum benefit 
    from this mathematical sequence that was uncovered in the Western world
    more than 800 years ago. Let's tackle the subject with a quick Fibonacci primer
    and then get down to business with two original strategies that
    tap directly into its hidden power. 

    https://www.investopedia.com/articles/markets/010515/use-fibonacci-point-out-profitable-trades.asp

    Args:
        candles(pandas.DataFrame): all columns.
    """

    def __init__(
        self,
        candles: pd.DataFrame,
    ):
        self._high = candles['high']
        self._low = candles['low']
        self._candles = candles
        self._levels = [1, 0.786, 0.618, 0.5, 0.382, 0.236, 0]
        self._run()

    def _run(self):
        self._max_high = self._high.max()
        self._min_low = self._low.min()
        self._max_stamp = self._candles.loc[self._candles['high'] == self._max_high].timestamp.item()
        self._min_stamp = self._candles.loc[self._candles['low'] == self._min_low].timestamp.item()
        if self._min_stamp > self._max_stamp:
            self._pivot = self._level(self, self._min_low, self._max_high)
        else:
            self._pivot = self._level(self, self._max_high, self._min_low)

    @staticmethod
    def _level(self, start: float, finish: float) -> dict:
        result = {}
        for level in self._levels:
            result[str(level)] = start - ((start - finish) * level)
        return result

    def fibonacci(self):
        """Pivot Point Fibonacci

        Returns:
            dict: New feature generated.
        """
        return self._pivot
