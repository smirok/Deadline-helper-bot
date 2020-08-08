from aiogram import Dispatcher
from aiogram.types import ContentTypes
from state_machine import StateMachine

from .help import process_help
from .start import process_start
from .others import process_choose_type, process_choose_subject, process_choose_task
from .others import process_choose_old_deadline, process_choose_new_deadline, process_show_info


def setup(dispatcher: Dispatcher):
    dispatcher.register_message_handler(process_start, commands=['start'])
    dispatcher.register_message_handler(process_help, commands=['help'])
    dispatcher.register_message_handler(process_choose_type,
                                        state='*', commands=['add', 'del', 'upd'])
    dispatcher.register_message_handler(process_choose_subject,
                                        state=StateMachine.waiting_for_subject,
                                        content_types=ContentTypes.TEXT
                                        )
    dispatcher.register_message_handler(process_choose_task,
                                        state=StateMachine.waiting_for_task,
                                        content_types=ContentTypes.TEXT
                                        )
    dispatcher.register_message_handler(process_choose_old_deadline,
                                        state=StateMachine.waiting_for_old_record,
                                        content_types=ContentTypes.TEXT
                                        )
    dispatcher.register_message_handler(process_choose_new_deadline,
                                        state=StateMachine.waiting_for_new_date)
    dispatcher.register_message_handler(process_show_info, commands=['show'])
