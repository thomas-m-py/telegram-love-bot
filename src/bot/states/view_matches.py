from aiogram.fsm.state import StatesGroup, State


class ViewMatchesForm(StatesGroup):
    view = State()
