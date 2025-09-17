from aiogram.fsm.state import StatesGroup, State


class DisableProfileForm(StatesGroup):
    disable = State()
