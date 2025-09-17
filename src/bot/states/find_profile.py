from aiogram.fsm.state import StatesGroup, State


class FindProfileForm(StatesGroup):
    find = State()
    create_match_with_message = State()
