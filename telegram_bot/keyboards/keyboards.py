from aiogram import types


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


return_kb = [
    [
        types.InlineKeyboardButton(text="Назад ⤴",
                                   callback_data="start")
    ]
]

return_keyboard = types.InlineKeyboardMarkup(
    inline_keyboard=return_kb
)
