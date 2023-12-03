from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    start_state = State()
    rubrics_state = State()
    phrases_state = State()
    generation_state = State()
