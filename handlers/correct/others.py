from aiogram.types import Message, ReplyKeyboardRemove, ContentTypes
from enum import Enum
from aiogram.dispatcher import FSMContext

from main import dispatcher
from keyboards import *
from database import Database, Query
from state_machine import StateMachine

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


@dispatcher.message_handler(state='*', commands=['add', 'del', 'upd'])
async def process_choose_type(message: Message, state: FSMContext):
    query_type = {
        '/add': QueryTypes.ADD,
        '/upd': QueryTypes.UPD,
        '/del': QueryTypes.DEL
    }.get(message.text, 0)
    await state.update_data(type=query_type)
    await message.answer('Выберите предмет', reply_markup=subjects)
    await StateMachine.waiting_for_subject.set()


@dispatcher.message_handler(state=StateMachine.waiting_for_subject,
                            content_types=ContentTypes.TEXT)
async def process_choose_subject(message: Message, state: FSMContext):
    if message.text not in subjects_to_tasks.keys():
        await message.reply('Выберите предмет, используя клавиатуру ниже.')
        return

    await state.update_data(subject=message.text)
    await message.answer('Выберите задание',
                         reply_markup=subjects_to_tasks[message.text])
    await StateMachine.waiting_for_task.set()


@dispatcher.message_handler(state=StateMachine.waiting_for_task,
                            content_types=ContentTypes.TEXT)
async def process_choose_task(message: Message, state: FSMContext):
    if message.text not in tasks:
        await message.reply('Выберите задание, используя клавиатуру ниже.')
        return

    await state.update_data(task=message.text)
    user_data = await state.get_data()

    if user_data['type'] == QueryTypes.ADD:
        await message.answer('Введите дату дедлайна в формате ДД.ММ.ГГГГ',
                             reply_markup=ReplyKeyboardRemove())
        await StateMachine.waiting_for_new_date.set()
    else:
        query = Query(user_data['subject'],
                      user_data['task'])
        deadlines = select_query_deadlines(query)
        if not deadlines:
            await message.answer(f'Изменять нечего :( \n'
                                 f'Дедлайнов нет', reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer('Выберите дедлайн',
                                 reply_markup=make_keyboard(select_query_deadlines(query)))
            await StateMachine.waiting_for_old_record.set()


@dispatcher.message_handler(state=StateMachine.waiting_for_old_record,
                            content_types=ContentTypes.TEXT)
async def process_choose_old_deadline(message: Message, state: FSMContext):
    user_data = await state.get_data()
    query = Query(user_data['subject'],
                  user_data['task'])
    if message.text not in select_query_deadlines(query):
        await message.reply('Выберите дедлайн, используя клавиатуру ниже')
    await state.update_data(deadline=message.text[-10:])
    user_data = await state.get_data()
    query = Query(user_data['subject'],
                  user_data['task'],
                  '.'.join(reversed(user_data['deadline'].split('.'))))
    if user_data['type'] == QueryTypes.DEL:
        Database.delete(query)
        await message.answer('Сделано', reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:  # QueryTypes.UPD
        await message.answer('Введите дату дедлайна в формате ДД.ММ.ГГГГ',
                             reply_markup=ReplyKeyboardRemove())
        await StateMachine.waiting_for_new_date.set()


@dispatcher.message_handler(state=StateMachine.waiting_for_new_date)
async def process_choose_new_deadline(message: Message, state: FSMContext):
    from re import match
    if match('\d{2}.\d{2}.\d{4}', message.text) is None:
        await message.reply('Дата не соотвествует формату\n'
                            'Введите дату в формате ДД.ММ.ГГГГ')
        return

    await state.update_data(new_deadline=str(message.text))
    user_data = await state.get_data()
    query = Query(user_data['subject'],
                  user_data['task'],
                  '.'.join(reversed(user_data['new_deadline'].split('.'))))
    if user_data['type'] == QueryTypes.ADD:
        Database.add(query)  # если уже есть ?
    else:  # QueryTypes.UPD or DEL
        Database.update(query, user_data['deadline'])

    await message.answer('Сделано')
    await state.finish()


@dispatcher.message_handler(commands=['show'])
async def process_show_info(message: Message):
    current_records = Database.show().split('\n')
    answer_message = ['%i. %s' % (number + 1, record)
                      for number, record in enumerate(current_records)]
    if not answer_message:
        answer_message = ['Дедлайнов нет:)']
    await message.answer('\n'.join(answer_message))
