from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.bot.handlers.helpers.show_menu import show_menu
from src.bot.handlers.helpers.show_profile import build_profile
from src.modules.profile.domain.profile.errors import ProfileNotFoundError
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.profile.use_cases.get_next_profile import (
    ResolveProfileState,
    ResolveProfile,
)
from src.modules.user.domain.types import TUserId


async def get_next_profile(
    profile_repository: ProfileRepository,
    message: Message,
    i18n: I18nContext,
    skip: bool = True,
):
    state_ = ResolveProfileState(
        user_id=TUserId(message.from_user.id), skip_current=skip
    )
    next_prof = ResolveProfile(profile_repository=profile_repository)

    try:
        await next_prof(state_)
    except ProfileNotFoundError:
        await message.answer(i18n.need_create_profile())
        return

    next_profile = state_.next_profile
    if next_profile is None:
        await message.answer(i18n.no_profiles())
        await show_menu(
            message=message,
            i18n=i18n,
        )
        return False
    await message.answer_media_group(build_profile(next_profile).build())
    return True
