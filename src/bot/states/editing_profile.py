from aiogram.fsm.state import StatesGroup, State


class MyProfileForm(StatesGroup):
    view = State()
    edit_bio = State()
    edit_media = State()
