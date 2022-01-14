import json
import websocket
import time

symbol = 'btcusd'
timeframe = '1m'

socket = f'wss://stream.binance.com:9443/ws/{symbol}t@kline_{timeframe}'


def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']

    if is_candle_closed:
        print(candle)
        json.dump(candle, 'candles_data.json')
        # close = candle['c']
        # high = candle['h']
        # low = candle['l']
        # vol = candle['v']
        #
        # print(close)
        # print(high)
        # print(low)
        # print(vol)


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)

if __name__ == '__main__':
    ws.run_forever()
