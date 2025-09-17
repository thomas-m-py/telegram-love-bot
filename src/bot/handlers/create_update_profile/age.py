from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.bot.utils.keyboard import build_reply_keyboard
from src.bot.states.create_profile import CreateProfileForm
from src.modules.profile.domain.profile.errors import (
    AgeRestrictionError,
    NotRealAgeError,
)
from src.modules.profile.domain.profile.value_objects.age import Age

router = Router()


@router.message(F.text, CreateProfileForm.age)
async def handle_age_input(message: Message, i18n: I18nContext, state: FSMContext):
    try:
        age_value = int(message.text)
    except ValueError:
        await message.answer(i18n.enter_number_age())
        return

    try:
        Age.create(age_value)
    except AgeRestrictionError:
        await message.answer(i18n.age_restriction())
        return
    except NotRealAgeError:
        await message.answer(i18n.enter_real_age())
        return

    await state.update_data(age=age_value)
    await state.set_state(CreateProfileForm.sex)

    await message.answer(
        i18n.choice_your_sex(),
        reply_markup=build_reply_keyboard(i18n.i_am_men(), i18n.i_am_woman()),
    )
