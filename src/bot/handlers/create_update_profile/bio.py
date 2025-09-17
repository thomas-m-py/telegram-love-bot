from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy

from src.bot.utils.keyboard import build_reply_keyboard
from src.bot.states.create_profile import CreateProfileForm
from src.modules.profile.domain.profile.errors import BioTooShortError, BioTooLongError
from src.modules.profile.domain.profile.value_objects.bio import Bio

router = Router()


async def transition_to_media_input(
    message: Message, i18n: I18nContext, state: FSMContext
):
    await state.set_state(CreateProfileForm.media)

    state_data = await state.get_data()
    has_previous_media = state_data.get("prev_media") is not None

    if has_previous_media:
        keyboard = build_reply_keyboard(i18n.leave_previous())
    else:
        keyboard = build_reply_keyboard(i18n.choice_from_telegram_account())

    await message.answer(i18n.send_media(), reply_markup=keyboard)


@router.message(
    F.text.in_((LazyProxy("skip"), LazyProxy("leave_previous"))), CreateProfileForm.bio
)
async def handle_bio_input(message: Message, i18n: I18nContext, state: FSMContext):
    await transition_to_media_input(message, i18n, state)


@router.message(F.text, CreateProfileForm.bio)
async def handle_bio_input(message: Message, i18n: I18nContext, state: FSMContext):

    bio_text = message.text
    try:
        Bio.create(bio_text)
    except BioTooShortError:
        await message.answer(i18n.bio_short())
        return
    except BioTooLongError:
        await message.answer(i18n.bio_long())
        return

    await state.update_data(bio=bio_text)
    await transition_to_media_input(message, i18n, state)
