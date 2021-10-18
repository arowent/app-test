import asyncio

import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
from termcolor import colored
from ta import momentum, trend
import time

from logger import logger


async def get_candels(ticker, timeframe):
    """Забираем свечи с binance"""

    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=500)
    await asyncio.sleep(0)

    return result

async def get_data():
    tickers = ['BTC/USDT', 'ETH/USDT']
    timeframes = ['5m', '15m']
    start_time = time.perf_counter()

    for ticker in tickers:
        logger.debug(f'ticker = {ticker}')
        for timeframe in timeframes:
            logger.debug(f'timeframe = {timeframe}')
            
            table = get_candels(ticker, timeframe)
            logger.info(f'TABLE: {table[0]}\n')
            await data_recording(table)

    logger.info(f'[FINISH] {time.perf_counter() - start_time}')


async def data_recording(data):
    try:
        with open(r'../tradingview/data_table.txt', 'w') as file:
            for i in data:
                file.write(str(i) + '\n')
    except Exception as err:
        logger.error(f'Не получилось записать данные в файл! '
                     f'ERROR: {err.__str__()}')

async def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_data())
    loop.close()


if __name__ == '__main__':
    asyncio.run(main())