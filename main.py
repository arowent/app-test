from statistics import median
import pandas as pd
import numpy as np
from ta import momentum, trend



class Average:
    def __init__(
        self, 
        price: list, 
        window: int = 2,
    ):
        self._price = price,
        self._window = window,

    def get_median(self):
        median_price = self._price
        return median_price


price = np.arange(10)
print(f'np.arange(10): {price} | type({type(price)})')
print(Average(price).get_median())
# print(price)