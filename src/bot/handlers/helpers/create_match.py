from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.bot.handlers.helpers.send_user_matches_count import send_matches_count
from src.modules.match.domain.match.errors import MatchCreationNotAllowedError
from src.modules.match.infra.db.match_repository import MatchRepository
from src.modules.match.domain.match.value_objects.message import Message as MatchMessage
from src.modules.match.use_cases.create_match import CreateMatchState, CreateMatchCase
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.user.infra.db.user_repository import UserRepository


async def create_match(
    message: Message,
    i18n: I18nContext,
    match_repository: MatchRepository,
    profile_repository: ProfileRepository,
    user_repository: UserRepository,
    profile_id: int,
    match_message: MatchMessage | None = None,
):
    my_profile = await profile_repository.find_by_user_id(profile_id)
    if my_profile is None:
        return

    state = CreateMatchState(
        from_profile_id=my_profile.user_id,
        to_profile_id=my_profile.profile_cursor,
        message=match_message,
    )
    create = CreateMatchCase(match_repository=match_repository)
    try:
        await create(state)
    except MatchCreationNotAllowedError:
        return

    await send_matches_count(
        bot=message.bot,
        i18n=i18n,
        match_repository=match_repository,
        profile_repository=profile_repository,
        user_repository=user_repository,
        user_id=my_profile.profile_cursor,
    )
