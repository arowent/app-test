import asyncio
import time
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
from logger import logger


async def get_candels(ticker, timeframe):
    """ Забираем свечи с binance """

    print('Running in get_candels()')
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=500)

    await writing_to_file(result)

    return result


async def writing_to_file(data):
    """ Запись данный в файл """

    try:
        print('Writing to a file')
        with open('data_table.txt', 'w') as file:
            for i in data:
                file.write(str(i) + '\n')
    except Exception as err:
        logger.error(f'Не получилось записать данные в файл!\nERROR: {err.__str__()}')


if __name__ == '__main__':
    start_time = time.perf_counter()
    # result = get_candels('BTC/USDT', '5m')
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(get_candels('BTC/USDT', '5m')), loop.create_task(writing_to_file())]
    loop.run_until_complete(asyncio.wait(task))
    loop.close()
    print(f'FINISH: {time.perf_counter() - start_time}')

