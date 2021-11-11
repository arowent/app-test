import asyncio
import time
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
from ta import momentum, trend


async def get_candels(ticker, timeframe):
    """Забираем свечи с binance"""
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(ticker, timeframe=timeframe, limit=100)

    return result


async def calculation_ema(close, window=5):
    """
    Формирование EMA
    и добавление нового столбца в DataFrame Pandas ["ema"]
    """
    ema_object = trend.EMAIndicator(close, window, fillna=True)
    ema = ema_object.ema_indicator()

    return ema.round(4)


async def calculation_tsi(close, longlen=20, shortlen=5):
    """
    Формирование Stochastic Oscillator и его сигнала
    добавление нового столбца в DataFrame Pandas ["tsi"]
    """
    tsi_object = momentum.tsi(close, window_slow=longlen, window_fast=shortlen, fillna=True) / 100

    return tsi_object.round(4)


async def calculation_signal(tsi, ema):
    """Формирование сигнала гистограммы"""
    signal = tsi - ema

    return signal.round(4)


async def creating_dataframe(candles):
    """Формирование полученных свечей в DataFrame"""
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%d.%m.%Y %H:%M'))
        open_data.append(candle[1])
        high_data.append(candle[2])
        low_data.append(candle[3])
        close_data.append(candle[4])
        # volume_data.append(candle[5])

    result = pd.DataFrame(data={
        'dates': dates,
        'open': open_data,
        'high': high_data,
        'low': low_data,
        'close': close_data,
        # 'volume': volume_data,
    })

    result['ema'] = await calculation_ema(result['close'])
    result['tsi'] = await calculation_tsi(result['close'])
    result['signal'] = await calculation_signal(result['tsi'], result['ema'])


    return result


async def main():
    start_time = time.perf_counter()
    symbols = ['BTC/USDT',]
    timeframes = ['5m', '30m', '6h',]
    
    for symbol in symbols:
        # print(f'Symbol: {symbol}')
        for timeframe in timeframes:
            # print(f'Timeframe: {timeframe}')
            candles = await get_candels(symbol, timeframe)
            dataframe = await creating_dataframe(candles)
            print(f'Symbol: {symbol} | Timeframe: {timeframe} | Status: Ok!')

    print(f'\nFinish: {time.perf_counter() - start_time}\n')



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    