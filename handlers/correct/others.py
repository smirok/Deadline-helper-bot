from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from enum import Enum

from main import dispatcher
from keyboards import *
from database import Database, Query

subjects_to_tasks = {
    'Haskell': haskell_tasks,
    'Алгосы': algorithms_tasks,
    'Алгебра': algebra_tasks,
    'Формальные языки': formal_languages_tasks,
    'Майнор': minor_tasks,
    'Матан': calculus_tasks
}

tasks = set()
for row in map(lambda elem: elem.keyboard, subjects_to_tasks.values()):
    for button in row:
        for values in button:
            tasks.add(values['text'])


class QueryTypes(Enum):
    ADD = 1
    UPD = 2
    DEL = 3


class QueryConstructor:
    type = None
    subject = None
    task = None
    deadline = None


@dispatcher.message_handler(commands=['add', 'del', 'upd'])
async def process_choose_subject(message: Message):
    QueryConstructor.type = {
        '/add': QueryTypes.ADD,
        '/upd': QueryTypes.UPD,
        '/del': QueryTypes.DEL
    }.get(message.text, 0)
    await message.answer('Выберите предмет', reply_markup=subjects)


@dispatcher.message_handler(Text(equals=subjects_to_tasks.keys()))
async def process_choose_task(message: Message):
    QueryConstructor.subject = message.text
    await message.answer('Выберите задание',
                         reply_markup=subjects_to_tasks[message.text])


@dispatcher.message_handler(Text(equals=tasks))
async def process_deadline_date(message: Message):
    QueryConstructor.task = message.text
    if QueryConstructor.type != QueryTypes.DEL:
        await message.answer('Введите дату дедлайна в формате ДД.ММ.ГГГГ',
                             reply_markup=ReplyKeyboardRemove())
    else:
        Database.delete(Query(QueryConstructor.subject,
                              QueryConstructor.task))
        await message.answer(f'Дедлайн {QueryConstructor.task} '
                             f'по предмету {QueryConstructor.subject} '
                             f'удалён', reply_markup=ReplyKeyboardRemove())


@dispatcher.message_handler(regexp='\d{2}.\d{2}.\d{4}')
async def process_last_input(message: Message):
    QueryConstructor.deadline = str(message.text)
    query = Query(QueryConstructor.subject,
                  QueryConstructor.task,
                  '.'.join(reversed(QueryConstructor.deadline.split('.'))))
    if QueryConstructor.type == QueryTypes.ADD:
        Database.add(query)
    else:  # QueryTypes.UPD
        Database.update(query)
    await message.answer('Сделано')


@dispatcher.message_handler(commands=['show'])
async def process_show_info(message: Message):
    await message.answer(Database.show())
