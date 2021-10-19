import asyncio
import numpy as np
import random
import time
from termcolor import colored


def get_numbers(data):
    result = np.random.random(data)

    return result


def writing_file(data):
    with open('test.txt', 'w') as file:
        for i in data:
            file.write(str(i) + '\n')


def main():
    number = 10000
    one_numbers = get_numbers(number)
    writing_file(one_numbers)

    return one_numbers


if __name__ == '__main__':
    start_time = time.perf_counter()
    # print(main())
    print(colored(f'FINISH: {time.perf_counter() - start_time}', 'yellow', attrs=['bold']))
