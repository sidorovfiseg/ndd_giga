from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
import telegram_bot.keyboards.keyboards as kb
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram_bot.keyboards.keyboards import return_keyboard

from giga_util.giga_search import Egor

router = Router()


class UserState(StatesGroup):
    start_state = State()
    rubrics_state = State()
    phrases_state = State()
    generation_state = State()


@router.message(Command("start"))
async def start_message(msg: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Начать работу ✅",
        callback_data="start"
    ))
    await msg.answer("Привет! Чтобы получить краткую аннатацию по патенту - нажмите на кнопку \"Начать работу ✅\" ниже ⤵", reply_markup=builder.as_markup())


@router.callback_query(F.data == "start")
async def handle_start_button(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if "count" in user_data:
        await state.set_data({"count": user_data["count"]})
    else:
        await state.set_data({"count": 1})
    await callback.message.answer(text="1 Шаг. Введите запрос по патенту.")

    await state.set_state(UserState.rubrics_state)
    await callback.answer()




@router.message(UserState.rubrics_state, F.text)
async def process_rubrics(msg: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="skip"
    ))
    await state.update_data(req = msg.text)

    await msg.answer("2 ШАГ. Введите 2 даты диапазона поиска или нажмите пропустить. Формат: 2 аты через пробел ез кавычек: '20000101 20100101': ",
                     reply_markup = builder.as_markup())
    await state.set_state(UserState.generation_state)

# Генерация патента TODO доделать генерацию


@router.callback_query(UserState.generation_state, F.data == 'skip')
async def handle_skip_button(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(dates = '20000101 20100101')
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Отменить ❌",
        callback_data="cancel_generation"
    ))

    gen_msg = await callback.message.answer(
        "Генерируем..., подождите 5 мин. 🕐", reply_markup=builder.as_markup()
    )

    req = user_data.get("req")
    dates = user_data.get("dates")

    print(user_data.get("req"))
    print(user_data.get("dates"))

    try:
        if dates != []:
            d1, d2 = dates.split()
            splitted_text = Egor(req, d1, d2)
        else:
            splitted_text = Egor(req)


        await gen_msg.edit_text(f"Аннотация №{user_data['count']}:", reply_markup=None)
        await state.set_state(UserState.phrases_state)
        user_data["count"] += 1
        await state.update_data(user_data)
        for i in range(len(splitted_text)):
            await callback.message.answer(f"{splitted_text[i]}")

    except Exception as e:
        # Обработка любого исключения и вывод текста ошибки
        await callback.message.answer("По запросу ничего не найдено")

    another_builder = InlineKeyboardBuilder()
    another_builder.add(types.InlineKeyboardButton(
        text="Начать заново",
        callback_data="start"
    ))
    await callback.message.answer("Нажмите на кнопку, чтобы начать заново", reply_markup=another_builder.as_markup())


@router.message(UserState.generation_state, F.text)
async def generate_patent(msg: Message, state: FSMContext):
    await state.update_data(dates = msg.text)
    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Отменить ❌",
        callback_data="cancel_generation"
    ))

    gen_msg = await msg.answer(
        "Генерируем..., подождите 5 мин. 🕐", reply_markup=builder.as_markup()
    )

    req = user_data.get("req")
    dates = user_data.get("dates")

    print(user_data.get("req"))
    print(user_data.get("dates"))

    try:
        if dates != []:
            d1, d2 = dates.split()
            splitted_text = Egor(req, d1, d2)
        else:
            splitted_text = Egor(req)

        await gen_msg.edit_text(f"Аннотация №{user_data['count']}:", reply_markup=None)
        await state.set_state(UserState.phrases_state)
        user_data["count"] += 1
        await state.update_data(user_data)
        for i in range(len(splitted_text)):
            await msg.answer(f"{splitted_text[i]}")

    except Exception as e:
        # Обработка любого исключения и вывод текста ошибки
        await msg.answer("По запросу ничего не найдено")

    another_builder = InlineKeyboardBuilder()
    another_builder.add(types.InlineKeyboardButton(
        text="Начать заново",
        callback_data="start"
    ))
    await msg.answer("Нажмите на кнопку, чтобы начать заново", reply_markup=another_builder.as_markup())




