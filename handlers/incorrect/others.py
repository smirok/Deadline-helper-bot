from main import dispatcher
from aiogram.types import Message


@dispatcher.message_handler()
async def kek(message: Message):
    await message.answer('Не знаете с чего начать? Воспользуйтесь командой /help')
