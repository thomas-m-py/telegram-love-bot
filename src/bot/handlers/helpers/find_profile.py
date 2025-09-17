from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram_i18n import I18nContext

from src.bot.handlers.helpers.get_next_profile import get_next_profile
from src.bot.states.find_profile import FindProfileForm
from src.bot.utils.keyboard import build_reply_keyboard
from src.modules.profile.infra.db.profile_repository import ProfileRepository


def build_find_profile_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    return build_reply_keyboard(
        i18n.like_profile_button_text(),
        i18n.like_with_message_profile_button_text(),
        i18n.dislike_profile_button_text(),
        i18n.waiting_likes_button_text(),
    )


async def find_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: ProfileRepository,
    skip: bool = False,
) -> None:

    await message.answer("🔍", reply_markup=build_find_profile_keyboard(i18n))
    has_profile = await get_next_profile(
        profile_repository=profile_repository, message=message, i18n=i18n, skip=skip
    )
    if has_profile:
        await state.set_state(FindProfileForm.find)
    else:
        await state.clear()
