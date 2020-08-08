from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

subjects_kb = ReplyKeyboardMarkup(
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

algorithms_tasks_kb = ReplyKeyboardMarkup(
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

haskell_tasks_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='???')
        ]
    ],
    resize_keyboard=True
)

formal_languages_tasks_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='???')
        ]
    ],
    resize_keyboard=True
)

calculus_tasks_kb = ReplyKeyboardMarkup(
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

algebra_tasks_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ДЗ')
        ]
    ],
    resize_keyboard=True
)

minor_tasks_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='???')
        ]
    ],
    resize_keyboard=True
)


def make_keyboard(picked_deadlines: List[str]) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(selective=True, resize_keyboard=True)
    for deadline in picked_deadlines:
        markup.add(f'{deadline}')
    return markup
