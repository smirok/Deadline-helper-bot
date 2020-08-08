from aiogram.types import Message, ReplyKeyboardRemove, ContentTypes
from aiogram.dispatcher import FSMContext
from enum import Enum

from main import dispatcher
from keyboards import subjects_kb, haskell_tasks_kb, algorithms_tasks_kb, \
    algebra_tasks_kb, formal_languages_tasks_kb, minor_tasks_kb, calculus_tasks_kb, \
    make_keyboard
from database import Database, Query
from state_machine import StateMachine

subjects_to_tasks = {
    'Haskell': haskell_tasks_kb,
    'Алгосы': algorithms_tasks_kb,
    'Алгебра': algebra_tasks_kb,
    'Формальные языки': formal_languages_tasks_kb,
    'Майнор': minor_tasks_kb,
    'Матан': calculus_tasks_kb
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
    await message.answer('Выберите предмет', reply_markup=subjects_kb)
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
    else:  # DEL OR UPD
        deadlines = Database.show(subject=user_data['subject'], task=user_data['task'])
        if not deadlines:
            await message.answer(f'По предмету {user_data["subject"]}, '
                                 f'заданию {user_data["task"]} дедлайнов нет\n'
                                 f'Попробуйте что-нибудь другое',
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer('Выберите дедлайн',
                                 reply_markup=make_keyboard(deadlines))
            await StateMachine.waiting_for_old_record.set()


@dispatcher.message_handler(state=StateMachine.waiting_for_old_record,
                            content_types=ContentTypes.TEXT)
async def process_choose_old_deadline(message: Message, state: FSMContext):
    user_data = await state.get_data()

    if message.text not in Database.show(subject=user_data['subject'],
                                         task=user_data['task']):
        await message.reply('Выберите дедлайн, используя клавиатуру ниже')
        return

    deadline = message.text[-10:]
    await state.update_data(deadline=deadline)
    user_data = await state.get_data()
    query = Query(subject=user_data['subject'],
                  task=user_data['task'],
                  deadline='.'.join(reversed(user_data['deadline'].split('.'))))
    if user_data['type'] == QueryTypes.DEL:
        Database.delete(query)
        await message.answer(f'Дедлайн {user_data["task"]} '
                             f'по предмету {user_data["subject"]} '
                             f'от {user_data["deadline"]} был удален',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:  # QueryTypes.UPD
        await message.answer('Введите дату дедлайна в формате ДД.ММ.ГГГГ',
                             reply_markup=ReplyKeyboardRemove())
        await StateMachine.waiting_for_new_date.set()


@dispatcher.message_handler(state=StateMachine.waiting_for_new_date)
async def process_choose_new_deadline(message: Message, state: FSMContext):
    from re import match
    if match('\\d{2}.\\d{2}.\\d{4}', message.text) is None:
        await message.reply('Дата не соотвествует формату\n'
                            'Введите дату в формате ДД.ММ.ГГГГ')
        return

    await state.update_data(new_deadline=str(message.text))
    user_data = await state.get_data()
    query = Query(subject=user_data['subject'],
                  task=user_data['task'],
                  deadline='.'.join(reversed(user_data['new_deadline'].split('.'))))
    if user_data['type'] == QueryTypes.ADD:
        Database.add(query)
        await message.answer(f'Дедлайн {user_data["task"]} '
                             f'по предмету {user_data["subject"]} '
                             f'от {user_data["new_deadline"]} был добавлен')
    else:  # QueryTypes.UPD or DEL
        Database.update(query, user_data['deadline'])
        await message.answer(f'Дедлайн {user_data["task"]} '
                             f'по предмету {user_data["subject"]} '
                             f'был перенесён с {user_data["deadline"]} '
                             f'на {user_data["new_deadline"]}')

    await state.finish()


@dispatcher.message_handler(commands=['show'])
async def process_show_info(message: Message):
    current_records = Database.show(subject=None, task=None)
    answer_message = ['%i. %s' % (number + 1, record)
                      for number, record in enumerate(current_records)]
    if not answer_message:
        answer_message = ['Дедлайнов нет:)']
    await message.answer('Текущие дедлайны:\n' + '\n'.join(answer_message))
