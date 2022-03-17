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
import numpy as np


class Point(object):
    __instance = None

    def __call__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

    def fullname(self):
        return 'Hello, {} {}!'.format(self.name, self.lastname)


pt = Point('Aloha', 'Lopatko')
pt2 = Point('Arowent', 'Lopatko')

print(pt.fullname())
print(pt2.fullname())
