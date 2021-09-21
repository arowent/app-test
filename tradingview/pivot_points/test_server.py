import sys
import ccxt
from datetime import datetime
import pandas as pd
import numpy as np
import portion as P
from ta import momentum
import time

from signals.models import (CandlesBTCUSD,
                            StrategyTimeframes,
                            Symbols,
                            Indicators,
                            IndicatorsSignals,
                            StochasticSignals,
                            StochasticSignalsLineD,
                            PivotPoints)

from config.logger import logger

def get_tickers():
    """Получаем все символы из БД"""
    result = Symbols.objects.all()
    return result

def get_indicators():
    """Получаем все индикаторы из БД"""
    return Indicators.objects.all()

def get_candels(time_frame, ticker):
    """Получаем набор свечей в зависимости от входящих параметров"""
    result = CandlesBTCUSD.objects.filter(timeframe=time_frame, symbol=ticker).values_list('candle_stamp',
                                                                                           'open',
                                                                                           'high',
                                                                                           'low',
                                                                                           'close',
                                                                                           'volume',
                                                                                           'timeframe',
                                                                                           'symbol'
                                                                                           ).order_by('candle_stamp')

    return result

def get_candels_dataframe(timeframe, ticker):
    '''Формирование полученных свечей в DataFrame'''
    candles = get_candels(timeframe, ticker)

    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    # volume_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%d-%m-%Y %H:%M'))
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

    # result.to_excel('pivot_points.xlsx')

    return result

def pivote_classic(Close, High, Low):
    PP = (High + Low + Close) / 3
    R1 = 2 * PP - Low
    S1 = 2 * PP - High
    R2 = PP + (High - Low)
    S2 = PP - (High - Low)
    R3 = PP + 2 * (High - Low)
    S3 = PP - 2 * (High - Low)

    pivot = []
    pivot.append(S3.round(4))
    pivot.append(S2.round(4))
    pivot.append(S1.round(4))
    pivot.append(PP.round(4))
    pivot.append(R1.round(4))
    pivot.append(R2.round(4))
    pivot.append(R3.round(4))

    return pivot

def pivot_fibonacci(Close, High, Low):
    PP = (High + Low + Close) / 3
    R1 = PP + (0.382 * (High - Low))
    S1 = PP - (0.382 * (High - Low))
    R2 = PP + (0.618 * (High - Low))
    S2 = PP - (0.618 * (High - Low))
    R3 = PP + (1.000 * (High - Low))
    S3 = PP - (1.000 * (High - Low))

    pivot = []
    pivot.append(S3.round(4))
    pivot.append(S2.round(4))
    pivot.append(S1.round(4))
    pivot.append(PP.round(4))
    pivot.append(R1.round(4))
    pivot.append(R2.round(4))
    pivot.append(R3.round(4))

    return pivot

def pivot_camarillo(Close, High, Low):
    PP = (High + Low + Close) / 3
    R1 = Close + ((High - Low) * 1.0833)
    S1 = Close - ((High - Low) * 1.0833)
    R2 = Close + ((High - Low) * 1.1666)
    S2 = Close - ((High - Low) * 1.1666)
    R3 = Close + ((High - Low) * 1.2500)
    S3 = Close - ((High - Low) * 1.2500)

    pivot = []
    pivot.append(S3.round(4))
    pivot.append(S2.round(4))
    pivot.append(S1.round(4))
    pivot.append(PP.round(4))
    pivot.append(R1.round(4))
    pivot.append(R2.round(4))
    pivot.append(R3.round(4))

    return pivot

def pivot_woody(Close, High, Low):
    PP = (High + Low + (2 * Close)) / 4
    R1 = (2 * PP) - Low
    S1 = (2 * PP) - High
    R2 = PP + High - Low
    S2 = PP - High + Low
    R3 = None
    S3 = None

    pivot = []
    pivot.append(S3)
    pivot.append(S2.round(4))
    pivot.append(S1.round(4))
    pivot.append(PP.round(4))
    pivot.append(R1.round(4))
    pivot.append(R2.round(4))
    pivot.append(R3)

    return pivot

def pivot_de_mark(Close, High, Low, Open):
    if Close < Open:
        PP = High + (2 * Low) + Close
    elif Close > Open:
        PP = (2 * High) + Low + Close
    elif Close == Open:
        PP = High + Low + (2 * Close)

    R1 = (PP / 2) + High
    S1 = (PP / 2) - Low
    R2 = None
    S2 = None
    R3 = None
    S3 = None

    pivot = []
    pivot.append(S3)
    pivot.append(S2)
    pivot.append(S1)
    pivot.append(PP)
    pivot.append(R1)
    pivot.append(R2)
    pivot.append(R3)

    return pivot

def pivot_frame(timeframe, ticker):
    start_frame = time.perf_counter()
    result = get_candels_dataframe(timeframe, ticker).tail(2).head(1)
    # print(result)
    ind = result.index[0]
    # print(f'IND = {ind}')
    # classic = pivote_classic(result['close'][498], result['high'][498], result['low'][498])
    classic = pd.Series(pivote_classic(result['close'][ind], result['high'][ind], result['low'][ind])).fillna("0")
    fibonacci = pd.Series(pivot_fibonacci(result['close'][ind], result['high'][ind], result['low'][ind])).fillna("0")
    camarillo = pd.Series(pivot_camarillo(result['close'][ind], result['high'][ind], result['low'][ind])).fillna("0")
    woody = pd.Series(pivot_woody(result['close'][ind], result['high'][ind], result['low'][ind])).fillna("0")
    de_mark = pd.Series(pivot_de_mark(result['close'][ind], result['high'][ind], result['low'][ind], result['open'][ind])).fillna("0")

    # colBase = ['S3', 'S2', 'S1', 'P', 'R1', 'R2', 'R3']
    # colums = ['Точки', 'Классические', 'Фибоначчи', 'Камарилья', 'Вуди', 'ДеМарк']

    # pivots = pd.DataFrame(zip(colBase, classic, fibonacci, camarillo, woody, de_mark), columns=colums).fillna('0')
    # logger.info(f'pivot_frame: {time.perf_counter() - start_frame}')

    return classic, fibonacci, camarillo, woody, de_mark

def get_pivot_points():
    print(f'DATE = {datetime.now().strftime("%I:%M%p on %B %d, %Y")}')
    start_pivot = time.perf_counter()
    tickers = get_tickers()
    # tickers = Symbols.objects.get(pk=1)
    # print(f'tickers = {tickers}')
    # indicator = Indicators.objects.get(pk=2)
    # print(f'symbol = {indicator}')
    trend = []
    timeframes = ['5m', '15m', '30m', '1h', '4h', '6h', '12h', '1d', '1w']
    # timeframes = ['1w']
    # print(f'timeframes = {timeframes}')
    for ticker in tickers:
        for timeframe in timeframes:
            start_one = time.perf_counter()
            if ticker == 8 and timeframe == '1w':
                break
            else:
                logger.info(f'{ticker} | {timeframe}')
                classic, fibonacci, camarillo, woody, de_mark = pivot_frame(timeframe, ticker) # Здесь вызывать метод. который вернет тренд
                # logger.info(f'Длина PP = {len(pp)}')
                # print(f'{ticker} | {timeframe}')
                # print(classic, "\n", fibonacci, "\n", camarillo, "\n", woody, "\n", de_mark)
                load_oscillator_signals_to_db(classic, fibonacci, camarillo, woody, de_mark, timeframe, ticker)
                logger.info(f'get_pivot: {time.perf_counter() - start_one}')
        logger.info(f'[FINISH] get_pivot_points: {time.perf_counter() - start_pivot}\n')
        # print(f'\n[FINISH] get_pivot_points: {time.perf_counter() - start_pivot}')

    return trend

def load_oscillator_signals_to_db(classic, fibonacci, camarillo, woody, de_mark, timeframe, ticker):
    try:
        labels = {'Классические': 'classic', 'Фибоначчи': 'fibonacci', 'Камарилья': 'camarillo',
                  'Вуди': 'woody', 'ДеМарк': 'de_mark'}
        numbers = {'Классические': classic, 'Фибоначчи': fibonacci, 'Камарилья': camarillo,
                   'Вуди': woody, 'ДеМарк': de_mark}
        colBase = ['S3', 'S2', 'S1', 'P', 'R1', 'R2', 'R3']
        columns = ['Классические', 'Фибоначчи', 'Камарилья', 'Вуди', 'ДеМарк']

        start_load = time.perf_counter()
        for column in columns:
            for index in range(len(colBase)):
                # print(colBase[index], numbers[column][index])
                new_row = PivotPoints.objects.update_or_create(
                    timeframe=timeframe,
                    symbol=ticker,
                    pivot_name=column,
                    pivot_dot=colBase[index],
                    label=labels[column],
                    defaults={
                        'pivot_value': numbers[column][index],
                    }
                )
        # for i in pp.loc[:, 'Классические':'ДеМарк']:
        #     for j in range(len(pp[i])):
        #         new_row = PivotPoints.objects.update_or_create(
        #             timeframe=timeframe,
        #             symbol=ticker,
        #             pivot_name=i,
        #             pivot_dot=pp['Точки'][j],
        #             label=labels[i],
        #             defaults={
        #                 'pivot_value': pp[i][j],
        #             }
        #         )
        logger.info(f'load_oscillator_signals_to_db: {time.perf_counter() - start_load}')

    except Exception as err:
        logger.error(f'Unexpected error: {err.__str__()}')
        # logger.debug("А запись то о загнале уже есть в БД!!!")