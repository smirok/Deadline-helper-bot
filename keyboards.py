from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
