from aiogram.fsm.state import StatesGroup, State


class CreateProfileForm(StatesGroup):
    age = State()
    sex = State()
    interest = State()
    city = State()
    confirm_city = State()
    name = State()
    bio = State()
    media = State()
    confirm = State()
