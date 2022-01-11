import aiogram
from aiogram import Bot, Dispatcher, executor, types
from lyricsbot.options import *
import logging
import requests

bot = Bot(token=TEST_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler()
async def echo(message: types.Message):
    logging.info(f'message: {message}')
    response = requests.get(f'http://api.musixmatch.com/ws/1.1/track.search?q_track={message.text}&apikey=b89801de465054369410e5cc778f7227')
    logging.info(f'message: {response.text}')
    # await message.answer(f'Your ID: {message["from"].id}')
    await message.answer(f'Your ID: {message.text}')


# auth_url = f'?&apikey={TOKEN}'
# url = 'https://api.musixmatch.com/ws/1.1/track.search?q_track'

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
