from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup
from aiogram.utils.link import create_tg_link
from aiogram_i18n import I18nContext, LazyProxy
from dishka import FromDishka

from src.bot.handlers.helpers.show_menu import show_menu
from src.bot.handlers.helpers.show_profile import build_profile
from src.bot.states.view_matches import ViewMatchesForm
from src.bot.utils.keyboard import build_reply_keyboard
from src.modules.match.domain.match.errors import (
    MatchNotFoundError,
    CannotMatchRejectedError,
    CannotRejectMatchedError,
)
from src.modules.match.infra.db.match_repository import MatchRepository
from src.modules.match.domain.match.value_objects.message import Message as MatchMessage
from src.modules.match.use_cases.accept_match import AcceptMatchState, AcceptMatchCase
from src.modules.match.use_cases.reject_match import RejectMatchState, RejectMatchCase
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.user.infra.db.user_repository import UserRepository

router = Router()


def build_match_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    return build_reply_keyboard(
        i18n.like_profile_button_text(),
        i18n.dislike_profile_button_text(),
        i18n.waiting_likes_button_text(),
    )


async def send_match_message(
    message: Message, i18n: I18nContext, match_message: MatchMessage
) -> None:

    if match_message.is_text():
        await message.answer(
            i18n.match_message_text_for_you(message_text=str(match_message))
        )
        return

    await message.answer_video(
        caption=i18n.match_message_video_for_you(),
        video=str(match_message),
        show_caption_above_media=True,
    )


async def send_match(
    message: Message,
    i18n: I18nContext,
    match_repository: MatchRepository,
    profile_repository: ProfileRepository,
    profile_id: int,
) -> bool:
    match = await match_repository.get_first_match_unseen(profile_id=profile_id)
    if match is None:
        await show_menu(
            message=message,
            i18n=i18n,
        )
        return False

    profile = await profile_repository.find_by_user_id(match.from_profile_id)
    await message.answer_media_group(build_profile(profile).build())

    if match.message:
        await send_match_message(
            message=message,
            i18n=i18n,
            match_message=match.message,
        )
    return True


@router.callback_query(F.data == "show_matches")
async def start_look_profiles(
    callback: CallbackQuery,
    i18n: I18nContext,
    state: FSMContext,
    match_repository: FromDishka[MatchRepository],
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await callback.message.answer("🔍", reply_markup=build_match_keyboard(i18n))
    has_match = await send_match(
        callback.message,
        i18n,
        match_repository,
        profile_repository,
        callback.from_user.id,
    )
    if has_match:
        await state.set_state(ViewMatchesForm.view)


@router.message(F.text == LazyProxy("like_profile_button_text"), ViewMatchesForm.view)
async def like_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    match_repository: FromDishka[MatchRepository],
    profile_repository: FromDishka[ProfileRepository],
    user_repository: FromDishka[UserRepository],
) -> None:

    match = await match_repository.get_first_match_unseen(
        profile_id=message.from_user.id
    )
    if match is None:
        await show_menu(
            message=message,
            i18n=i18n,
        )
        await state.clear()
        return

    state_ = AcceptMatchState(match_id=match.match_id)
    accept_case = AcceptMatchCase(match_repository=match_repository)
    try:
        await accept_case(state_)
    except (MatchNotFoundError, CannotMatchRejectedError):
        has_match = await send_match(
            message, i18n, match_repository, profile_repository, message.from_user.id
        )
        if not has_match:
            await state.clear()
        return

    user = await user_repository.find_by_tid(match.from_profile_id)
    url = create_tg_link("user", id=user.id)

    user_name = i18n.user_no_name()
    if user.last_name:
        user_name = f"{user.first_name} {user.last_name}"
    elif user.first_name:
        user_name = user.first_name

    await message.answer(
        i18n.matched_message_text(
            user_url=url,
            user_name=user_name,
            username=f"(@{user.username})" if user.username else "",
        )
    )
    try:
        with i18n.use_locale(user.language):
            await message.bot.send_message(
                chat_id=match.from_profile_id,
                text=i18n.matched_message_text(
                    user_url=message.from_user.url,
                    user_name=message.from_user.full_name,
                    username=(
                        f"(@{message.from_user.username})"
                        if message.from_user.username
                        else ""
                    ),
                ),
            )
    except TelegramBadRequest:
        pass

    has_match = await send_match(
        message, i18n, match_repository, profile_repository, message.from_user.id
    )
    if not has_match:
        await state.clear()


@router.message(
    F.text == LazyProxy("dislike_profile_button_text"), ViewMatchesForm.view
)
async def dislike_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    match_repository: FromDishka[MatchRepository],
    profile_repository: FromDishka[ProfileRepository],
) -> None:

    match = await match_repository.get_first_match_unseen(
        profile_id=message.from_user.id
    )
    state_ = RejectMatchState(match_id=match.match_id)
    reject_case = RejectMatchCase(match_repository=match_repository)
    try:
        await reject_case(state_)
    except (MatchNotFoundError, CannotRejectMatchedError):
        has_match = await send_match(
            message, i18n, match_repository, profile_repository, message.from_user.id
        )
        if not has_match:
            await state.clear()
        return

    has_match = await send_match(
        message, i18n, match_repository, profile_repository, message.from_user.id
    )
    if not has_match:
        await state.clear()


@router.message(F.text == LazyProxy("waiting_likes_button_text"), ViewMatchesForm.view)
async def sleep(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
) -> None:

    await show_menu(
        message=message,
        i18n=i18n,
    )
    await state.clear()
