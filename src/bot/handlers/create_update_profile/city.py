from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_i18n import I18nContext, LazyProxy

from src.bot.utils.keyboard import build_reply_keyboard
from src.bot.states.create_profile import CreateProfileForm
from src.modules.city.find_city import find_city

router = Router()


async def _ask_city_confirmation(
    message: Message, i18n: I18nContext, state: FSMContext, suggested_city: str
):
    await message.answer(
        i18n.did_you_mean(city=suggested_city),
        reply_markup=build_reply_keyboard(i18n.yes(), i18n.no_enter_again()),
    )
    await state.set_state(CreateProfileForm.confirm_city)


async def transition_to_name_input(
    message: Message, i18n: I18nContext, state: FSMContext
):
    await state.set_state(CreateProfileForm.name)

    state_data = await state.get_data()
    previous_name = state_data.get("name")
    keyboard = ReplyKeyboardRemove()
    if previous_name:
        keyboard = build_reply_keyboard(previous_name)

    await message.answer(i18n.enter_your_name(), reply_markup=keyboard)


@router.message(F.text, CreateProfileForm.city)
async def handle_city_input(message: Message, i18n: I18nContext, state: FSMContext):
    user_city_input = message.text
    resolved_city, is_exact_match = find_city(user_city_input)

    if resolved_city is None:
        await message.answer(i18n.enter_real_city())
        return

    await state.update_data(city=resolved_city)

    if not is_exact_match:
        await _ask_city_confirmation(message, i18n, state, resolved_city)
        return

    await transition_to_name_input(message, i18n, state)


@router.message(F.text == LazyProxy("yes"), CreateProfileForm.confirm_city)
async def handle_city_confirmation_yes(
    message: Message, i18n: I18nContext, state: FSMContext
):
    await transition_to_name_input(message, i18n, state)


@router.message(F.text == LazyProxy("no_enter_again"), CreateProfileForm.confirm_city)
async def handle_city_confirmation_no(
    message: Message, i18n: I18nContext, state: FSMContext
):
    await state.set_state(CreateProfileForm.city)
    await message.answer(i18n.enter_your_city(), reply_markup=ReplyKeyboardRemove())
