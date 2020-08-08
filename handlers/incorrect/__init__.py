from aiogram import Dispatcher

from .others import process_any_message


def setup(dispatcher: Dispatcher):
    dispatcher.register_message_handler(process_any_message)
