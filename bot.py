from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token='5124834812:AAFFjA59_uwsyYYi7sLp_9bIul4tSXfsPL4')
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
