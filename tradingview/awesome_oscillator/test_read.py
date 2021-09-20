import pandas as pd
import numpy as np
import portion as P
import ta.momentum
from termcolor import colored
from ta import momentum, trend


trend = pd.read_excel('last_trend.xlsx')
print(trend)