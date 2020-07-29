from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from main import dispatcher


@dispatcher.message_handler(CommandStart())
async def process_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n '
                         'Я помогу тебе контролировать дедлайны!')
