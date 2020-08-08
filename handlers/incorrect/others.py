from aiogram.types import Message
from main import dispatcher


@dispatcher.message_handler()
async def process_any_message(message: Message):
    await message.answer('Не знаете с чего начать? Воспользуйтесь командой /help')
