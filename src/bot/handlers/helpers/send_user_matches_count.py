from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from src.modules.match.infra.db.match_repository import MatchRepository
from src.modules.profile.domain.profile.value_objects.sex import Sex
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.user.infra.db.user_repository import UserRepository


async def send_matches_count(
    bot: Bot,
    i18n: I18nContext,
    match_repository: MatchRepository,
    profile_repository: ProfileRepository,
    user_repository: UserRepository,
    user_id: int,
):
    count = await match_repository.get_count_unseen_matches(user_id)
    if count == 0:
        return

    profile = await profile_repository.find_by_user_id(user_id)
    user = await user_repository.find_by_tid(user_id)

    with i18n.use_locale(locale=user.language):
        plural = ""
        if count > 1:
            if profile.interest == Sex.MALE:
                plural = i18n.males()
            elif profile.interest == Sex.FEMALE:
                plural = i18n.females()
            else:
                plural = i18n.males_females()

        if profile.sex == Sex.MALE:
            if count == 1:
                text = i18n.male_someone_liked_you()
            else:
                text = i18n.male_matches_count(count=count, plural=plural)
        else:
            if count == 1:
                text = i18n.female_someone_liked_you()
            else:
                text = i18n.female_matches_count(count=count, plural=plural)

        inline_ = InlineKeyboardBuilder()
        inline_.button(text=i18n.show_matches(), callback_data="show_matches")

    try:
        await bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=inline_.as_markup(),
        )
    except TelegramBadRequest:
        pass
