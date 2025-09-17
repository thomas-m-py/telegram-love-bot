from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext

from src.bot.utils.keyboard import build_reply_keyboard
from src.bot.states.create_profile import CreateProfileForm

router = Router()


async def transition_to_city_input(
    message: Message, i18n: I18nContext, state: FSMContext
):
    await state.set_state(CreateProfileForm.city)

    state_data = await state.get_data()
    previous_city = state_data.get("city")
    keyboard = ReplyKeyboardRemove()
    if previous_city:
        keyboard = build_reply_keyboard(previous_city)

    await message.answer(i18n.enter_your_city(), reply_markup=keyboard)


def parse_interest_from_choice(choice_text: str, i18n: I18nContext) -> int | None:
    if choice_text == i18n.interest_men():
        return 0
    elif choice_text == i18n.interest_woman():
        return 1
    elif choice_text == i18n.interest_doesnt_matter():
        return None
    return -1


@router.message(F.text, CreateProfileForm.interest)
async def handle_interest_selection(
    message: Message, i18n: I18nContext, state: FSMContext
):
    selected_interest = parse_interest_from_choice(message.text, i18n)

    if selected_interest == -1:
        await message.answer(i18n.choice_interest())
        return

    await state.update_data(interest=selected_interest)
    await transition_to_city_input(message, i18n, state)
