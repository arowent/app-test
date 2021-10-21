import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ Создание соединения с БД """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'База Данный создана, версия: {sqlite3.version}')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = '/home/user/Code/code/asyncio/test_db.db'

    sql_create_candles_table = """CREATE TABLE IF NOT EXISTS candles (
    id integer PRIMARY KEY,
    candle_stamp bigint,
    open
    high
    low
    close
    volume
    timeframe
    symbol
    )"""


if __name__ == '__main__':
    create_connection("test_db.db")
