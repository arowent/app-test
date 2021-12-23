import time
import datetime
import requests
import json
from fake_useragent import UserAgent
import fake_proxy


fake_proxy.get()

# ua = UserAgent()
# print(ua.chrome)
#
# user_agent = {
#     'User-Agent': ua.chrome,
# }


# proxies_dict = {
#         "http": "http://167.172.109.12:39452",
#         "https": "https://167.172.109.12:39452"
#     }
#
# response = requests.get('https://www.bitstamp.net/api/v2/ohlc/btcusd.json', headers=user_agent)


# file = open('headers.txt')
# number = 0

# for i in file:
#     headers = {
#     'User-Agent': f'{i}',
#     }
#     print(f'{number} - {i}')
#     number += 1

#     try:
#         response = requests.get('https://www.bitstamp.net/api/v2/ohlc/btcusd.json', headers=headers)
#     except Exception as err:
#         print(f'Unexpected error: {err.__str__()}\n')