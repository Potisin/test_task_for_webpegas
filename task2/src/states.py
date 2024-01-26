from aiogram.fsm.state import StatesGroup, State


class MainState(StatesGroup):
    name = State()
    url = State()