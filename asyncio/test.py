import asyncio
import numpy as np
import random
import time

import pandas as pd
from termcolor import colored


async def get_numbers(data):
    result = pd.DataFrame(np.arange(data))
    print(f'result расчитан')
    await asyncio.sleep(random.randint(0, 2) * 0.001)
    writing_file(result)

    return result


def writing_file(data):
    data.to_excel('data_db.xlsx')
    print('Данные записаны в файл')


async def message():
    print(f'Message 1')
    await asyncio.sleep(0)
    print(f'Message 2')

if __name__ == '__main__':
    start_time = time.perf_counter()
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(get_numbers(10000)),
        loop.create_task(message()),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    print(colored(f'FINISH: {time.perf_counter() - start_time}', 'yellow', attrs=['bold']))
