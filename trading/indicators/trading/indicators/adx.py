# Trading in the direction of a strong trend reduces risk
# and increases profit potential. The average directional index (ADX)
# is used to determine when the price is trending strongly. In many cases,
# it is the ultimate trend indicator. After all, the trend may be your
# friend, but it sure helps to know who your friends are. In this article,
# we'll examine the value of ADX as a trend strength indicator.

import pandas as pd


class ADX:
    def __init__(
        self,
        high: pd.Series,
        low: pd.Series,
        window: int = 14,
    ):
        self._high = high
        self._low = low
        self._window = window
        self._run()
    
    def _run(self):
        pass
