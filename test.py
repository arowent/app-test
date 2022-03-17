from urllib import response
import requests
import json

"""
Your user ID: 1081326703
Current chat ID: 1081326703
Forwarded from chat: -1001480116466
"""


bot_token = '5124834812:AAFFjA59_uwsyYYi7sLp_9bIul4tSXfsPL4'
chat_id = -1001480116466

requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bot_token), params=dict(
   chat_id=str(chat_id),
   text='You bitch!'
))