from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Database
import handlers

from cfg import API_TOKEN

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)


def on_startup(dp: Dispatcher):
    handlers.correct.setup(dp)
    handlers.incorrect.setup(dp)


if __name__ == '__main__':
    Database.init()
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup(dispatcher))
