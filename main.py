from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from database import Database

from cfg import API_TOKEN

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)


async def on_startup(dispatcher: Dispatcher):
    Database.init()


if __name__ == '__main__':
    from handlers import dispatcher
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
