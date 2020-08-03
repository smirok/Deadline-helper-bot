from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import Database, Query
from typing import List

subjects = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Алгосы'),
            KeyboardButton(text='Haskell')
        ],
        [
            KeyboardButton(text='Матан'),
            KeyboardButton(text='Алгебра')
        ],
        [
            KeyboardButton(text='Формальные языки'),
            KeyboardButton(text='Майнор')
        ]
    ],
    resize_keyboard=True
)

algorithms_tasks = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Контест')
        ],
        [
            KeyboardButton(text='Теор. ДЗ')
        ]
    ],
    resize_keyboard=True
)

haskell_tasks = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='???')
        ]
    ],
    resize_keyboard=True
)

formal_languages_tasks = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='???')
        ]
    ],
    resize_keyboard=True
)

calculus_tasks = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ДЗ')
        ],
        [
            KeyboardButton(text='КР')
        ]
    ],
    resize_keyboard=True
)

algebra_tasks = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ДЗ')
        ]
    ],
    resize_keyboard=True
)

minor_tasks = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='???')
        ]
    ],
    resize_keyboard=True
)


def select_query_deadlines(query: Query) -> List[str]:
    Database.cursor.execute("SELECT * FROM deadlines ORDER BY deadline ASC")
    picked_deadlines = []
    while True:
        row = Database.cursor.fetchone()

        if row is None:
            break

        if row[0] == query.subject and row[1] == query.task:
            picked_deadlines.append(f' {row[0]} {row[1]}'
                                    f' {".".join(reversed(row[2].split(".")))}\n')

    return picked_deadlines


def make_keyboard(picked_deadlines: List[str]):  # найти тип клавиатуры
    markup = ReplyKeyboardMarkup(selective=True, resize_keyboard=True)
    for deadline in picked_deadlines:
        markup.add(f'{deadline}')
    return markup
