from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy
from dishka import FromDishka

from src.bot.handlers.helpers.send_user_matches_count import send_matches_count
from src.bot.handlers.helpers.show_menu import show_menu
from src.bot.states.disable import DisableProfileForm
from src.bot.utils.keyboard import build_reply_keyboard
from src.modules.match.infra.db.match_repository import MatchRepository
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.profile.use_cases.deactivate_profile import (
    DeactivateProfileState,
    DeactivateProfileCase,
)
from src.modules.user.infra.db.user_repository import UserRepository

router = Router()


@router.message(F.text.in_([LazyProxy("menu_disable_my_profile_button_text")]))
async def start_disable_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
) -> None:
    await state.set_state(DisableProfileForm.disable)
    await message.answer(
        i18n.disable_profile_text(),
        reply_markup=build_reply_keyboard(i18n.disable_profile(), i18n.go_back()),
    )


@router.message(F.text == LazyProxy("go_back"), DisableProfileForm.disable)
async def go_back(
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


@router.message(F.text == LazyProxy("disable_profile"), DisableProfileForm.disable)
async def disable_profile(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await state.clear()
    state_ = DeactivateProfileState(
        profile_id=message.from_user.id,
    )
    deactivate_case = DeactivateProfileCase(
        profile_repository=profile_repository,
    )
    await deactivate_case(state_)
    await message.answer(
        i18n.goodbye_text(), reply_markup=build_reply_keyboard(i18n.look_profile_text())
    )
