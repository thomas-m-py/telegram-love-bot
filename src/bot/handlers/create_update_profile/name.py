from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.bot.utils.keyboard import build_reply_keyboard
from src.bot.states.create_profile import CreateProfileForm
from src.modules.profile.domain.profile.errors import NameTooLongError
from src.modules.profile.domain.profile.value_objects.name import Name

router = Router()


async def transition_to_bio_input(
    message: Message, i18n: I18nContext, state: FSMContext
):
    await state.set_state(CreateProfileForm.bio)

    state_data = await state.get_data()
    previous_bio = state_data.get("bio")

    keyboard = build_reply_keyboard(
        i18n.leave_previous() if previous_bio is not None else i18n.skip()
    )

    await message.answer(i18n.enter_bio(), reply_markup=keyboard)


@router.message(F.text, CreateProfileForm.name)
async def handle_name_input(message: Message, i18n: I18nContext, state: FSMContext):
    user_name = message.text

    try:
        Name.create(user_name)
    except NameTooLongError:
        await message.answer(i18n.enter_real_name())
        return

    await state.update_data(name=user_name)
    await transition_to_bio_input(message, i18n, state)
