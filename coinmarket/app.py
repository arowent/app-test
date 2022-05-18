from asyncio.log import logger
import json
import logging
import os
from os.path import dirname, join
from pprint import pprint
from urllib import response

import requests
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure environment
path = join(dirname(__file__), '.env')
load_dotenv(path)

COINMARKET_KEY = os.environ.get("COINMARKET_KEY")

url = 'https://developers.coinmarketcal.com/v1/events'


def connection_coinmarket(url: str):
    with requests.Session() as session:
        querystring = {"max":"10","coins":"bitcoin"}
        headers = {
            'x-api-key': COINMARKET_KEY,
            'Accept': "application/json"
        }
        response = session.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            text = json.loads(response.text)
            logging.info(f'Response json: {[(i.get("id"), i.get("title")) for i in text.get("body")]}')

    return None


connection_coinmarket(url)
