from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from database import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from cfg import API_TOKEN

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()  # потом переделать
dispatcher = Dispatcher(bot, storage=storage)


async def on_startup(dispatcher: Dispatcher):
    Database.init()


if __name__ == '__main__':
    from handlers import dispatcher

    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
