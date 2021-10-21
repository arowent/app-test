import asyncio
import time
import numpy as np
from termcolor import colored


def sync_example():
    numbers = np.arange(10, 20)
    new_numbers = []
    for i in numbers:
        new_numbers.append(i)

    return new_numbers


def sync_func():
    print('Запуск...')
    numbers = sync_example()
    print(numbers)
    print('... Готово!')


async def async_example():
    numbers = np.arange(10, 20)
    new_numbers = []
    for i in numbers:
        new_numbers.append(i)

    return new_numbers


async def async_func():
    print('Запуск...')
    numbers = await async_example()
    print(f'new_numbers: {numbers}')
    print('... Готово!')


async def main():
    await async_func()


def sync_main():
    sync_func()


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    # sync_main()
    print(colored(f'FINISH: {time.perf_counter() - start_time}', 'yellow', attrs=['bold']))
