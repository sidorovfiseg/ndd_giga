from aiogram import types

start_kb = [
    [
        types.KeyboardButton(text="Начать работу ✅"),
    ]
]

start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=start_kb,
    resize_keyboard=True,
    one_time_keyboard=True
)

rubrics_kb = [
    [
        types.KeyboardButton(text="Продолжить")
    ]
]

rubrics_keyboard = types.ReplyKeyboardMarkup(
    keyboard=rubrics_kb,
    resize_keyboard=True,
    one_time_keyboard=True
)

reload_kb = [
    [
        types.KeyboardButton(text="Начать заново")
    ]
]

reload_keyboard = types.ReplyKeyboardMarkup(
    keyboard=reload_kb,
    resize_keyboard=True,
    one_time_keyboard=True
)
