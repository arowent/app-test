import numpy as np

number = list(np.arange(10))
print(type(number))

def get_number_list(data):
    if isinstance(data, list):
        return [i*i for i in data]
    else:
        return 'не фига не работает'

print(get_number_list(number))
