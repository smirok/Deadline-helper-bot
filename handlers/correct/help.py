from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from main import dispatcher


@dispatcher.message_handler(CommandHelp())
async def process_help(message: types.Message):
    await message.answer('/add - добавить новый дедлайн\n'
                         '/update - изменить существующий дедлайн\n'
                         '/delete - удалить существующий дедлайн')
