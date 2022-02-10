import ccxt
from datetime import datetime
import pandas as pd
import content


def get_candles(symbol: str, timeframe: str = '1h', limit: int = 26) -> list:
    """Taking candles from binance"""
    binance = ccxt.binance()
    result = binance.fetch_ohlcv(symbol, timeframe, limit=limit)

    return result


def get_candles_dataframe(candles: list) -> pd.DataFrame:
    """Generating data in a DataFrame"""
    dates = list()
    close_data = list()

    for candle in reversed(candles):
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%d.%m.%Y %H:%M'))
        close_data.append(candle[4])

    result = pd.DataFrame(data={
        'dates': dates,
        'close': close_data,
    })

    result = result.drop(result.head(1).index.values[0])

    return result


def get_table(data: pd.DataFrame, ath: int) -> list:
    """ATH change item

    Creating a list of elements: price at a given time on the '1h' timeframe,
    percentage change in price, ATH price at a given time, percentage change in ATH.
    """
    price_current = data.head(1).close.values[0]  # price at the moment of time
    price_previous = data.tail(1).close.values[0]  # price for the previous week
    change_day = (((price_current - price_previous) / price_previous) * 100).round(2)  # price change
    change_ath = (((price_current - ath) / ath) * 100).round(2)  # ath change
    table = [price_current, change_day, ath, change_ath]

    return table


def main():
    """Summary tables on ATH correction

    From: https://bytwork.com/articles/ath

    This is the highest price value for the entire existence of the cryptocurrency.
    This indicator shows how much the price of a certain cryptocurrency or coin has
    fallen as a percentage. This percentage shows how much the coin has
    fallen from its recorded historical maximum.
    """
    symbols = content.symbols
    market = 'Binance'

    ticker = list()
    price_now = list()
    ath_day = list()
    store = list()
    ath_now = list()
    ath_correction = list()

    for symbol in symbols:
        print(f'symbol: {symbol}')
        candles = get_candles(symbol)
        result = get_candles_dataframe(candles)
        ath = content.aths[symbol]
        data = get_table(result, ath)

        ticker.append(symbol)
        price_now.append(data[0])
        ath_day.append(data[1])
        store.append(market)
        ath_now.append(data[2])
        ath_correction.append(data[3])

    result = pd.DataFrame(data={
        'ticker': ticker,
        'price_current': price_now,
        'percent': ath_day,
        'exchange': market,
        'ath_current': ath_now,
        'correction': ath_correction,
    })

    result.to_excel('table.xlsx', 'Группа 1 (Топ-альты)', index=False)
    # print(result)
    return 'Completed successfully!'


if __name__ == '__main__':
    main()
