from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy
from dishka import FromDishka

from src.bot.handlers.helpers.create_match import create_match
from src.bot.handlers.helpers.find_profile import find_profile
from src.bot.handlers.helpers.get_next_profile import get_next_profile
from src.bot.handlers.helpers.send_user_matches_count import send_matches_count
from src.bot.handlers.helpers.show_menu import show_menu
from src.bot.states.find_profile import FindProfileForm
from src.bot.utils.keyboard import build_reply_keyboard
from src.modules.match.infra.db.match_repository import MatchRepository
from src.modules.match.domain.match.value_objects.message import (
    Message as MatchMessage,
    MessageVideo,
)
from src.modules.profile.domain.profile.errors import ProfileNotFoundError
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.profile.use_cases.activate_profile import (
    ActivateProfileState,
    ActivateProfileCase,
)
from src.modules.user.infra.db.user_repository import UserRepository

router = Router()


@router.message(
    F.text.in_(
        [
            LazyProxy("look_profile_text"),
            LazyProxy("menu_start_find_profiles_button_text"),
        ]
    )
)
async def start_look_profiles(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    state_ = ActivateProfileState(profile_id=message.from_user.id)
    activate_case = ActivateProfileCase(profile_repository=profile_repository)
    try:
        await activate_case(state_)
    except ProfileNotFoundError:
        await message.answer(i18n.need_create_profile())
        return

    await find_profile(
        message=message, i18n=i18n, state=state, profile_repository=profile_repository
    )


@router.message(F.text == LazyProxy("like_profile_button_text"), FindProfileForm.find)
async def like(
    message: Message,
    i18n: I18nContext,
    profile_repository: FromDishka[ProfileRepository],
    match_repository: FromDishka[MatchRepository],
    user_repository: FromDishka[UserRepository],
) -> None:
    await create_match(
        message=message,
        i18n=i18n,
        match_repository=match_repository,
        profile_repository=profile_repository,
        user_repository=user_repository,
        profile_id=message.from_user.id,
    )
    await get_next_profile(
        profile_repository=profile_repository, message=message, i18n=i18n
    )


@router.message(
    F.text == LazyProxy("like_with_message_profile_button_text"), FindProfileForm.find
)
async def like_with_message(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
) -> None:
    await state.set_state(FindProfileForm.create_match_with_message)
    await message.answer(
        i18n.send_match_message(), reply_markup=build_reply_keyboard(i18n.go_back())
    )


@router.message(
    F.text == LazyProxy("go_back"), FindProfileForm.create_match_with_message
)
async def go_back(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await find_profile(
        message=message,
        i18n=i18n,
        state=state,
        profile_repository=profile_repository,
        skip=True,
    )


@router.message(F.text, FindProfileForm.create_match_with_message)
async def like_with_message_text(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
    match_repository: FromDishka[MatchRepository],
    user_repository: FromDishka[UserRepository],
) -> None:

    text = message.text
    await create_match(
        message=message,
        i18n=i18n,
        match_repository=match_repository,
        profile_repository=profile_repository,
        user_repository=user_repository,
        profile_id=message.from_user.id,
        match_message=MatchMessage.create(message=text),
    )
    await find_profile(
        message=message,
        i18n=i18n,
        state=state,
        profile_repository=profile_repository,
        skip=True,
    )


@router.message(F.video, FindProfileForm.create_match_with_message)
async def like_with_message_video(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
    match_repository: FromDishka[MatchRepository],
    user_repository: FromDishka[UserRepository],
) -> None:

    file_id = message.video.file_id
    await create_match(
        message=message,
        i18n=i18n,
        match_repository=match_repository,
        profile_repository=profile_repository,
        user_repository=user_repository,
        profile_id=message.from_user.id,
        match_message=MatchMessage.create(message=MessageVideo.create(file_id=file_id)),
    )
    await find_profile(
        message=message,
        i18n=i18n,
        state=state,
        profile_repository=profile_repository,
        skip=True,
    )


@router.message(
    F.text == LazyProxy("dislike_profile_button_text"), FindProfileForm.find
)
async def dislike(
    message: Message,
    i18n: I18nContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await get_next_profile(
        profile_repository=profile_repository, message=message, i18n=i18n
    )


@router.message(F.text == LazyProxy("waiting_likes_button_text"), FindProfileForm.find)
async def sleep(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
    match_repository: FromDishka[MatchRepository],
    user_repository: FromDishka[UserRepository],
) -> None:

    await message.answer(
        i18n.lets_wait(),
    )
    await show_menu(
        message=message,
        i18n=i18n,
    )
    await send_matches_count(
        bot=message.bot,
        i18n=i18n,
        match_repository=match_repository,
        profile_repository=profile_repository,
        user_repository=user_repository,
        user_id=message.from_user.id,
    )
    await state.clear()
