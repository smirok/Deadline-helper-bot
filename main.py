from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from cfg import API_TOKEN

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

if __name__ == '__main__':
    from handlers import dispatcher
    executor.start_polling(dispatcher, skip_updates=True)
