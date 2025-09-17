from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram_i18n import I18nContext
from dishka import FromDishka

from src.bot.handlers.helpers.show_menu import show_menu
from src.bot.handlers.helpers.show_profile import build_profile
from src.bot.utils.keyboard import build_reply_keyboard
from src.modules.profile.infra.db.profile_repository import ProfileRepository
from src.modules.user.domain.types import TUserId
from src.modules.user.infra.db.user_repository import UserRepository
from src.modules.user.use_cases.dto import UpdateUserDTO
from src.modules.user.use_cases.update_user import UpdateUserState, UpdateUserCase
from src.settings.const import LANGUAGES

router = Router()

languages_text = [lang for _, lang in LANGUAGES.items()]


def build_lang_kb():
    builder = ReplyKeyboardBuilder()
    for _, lang in LANGUAGES.items():
        builder.button(text=lang)
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)


def resolve_lang(message_text: str) -> str:
    for key, lang in LANGUAGES.items():
        if message_text == lang:
            return key


@router.message(Command("start"))
async def start_handler(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    profile_repository: FromDishka[ProfileRepository],
) -> None:
    await state.clear()

    profile = await profile_repository.find_by_user_id(TUserId(message.from_user.id))
    if not profile:
        await message.answer(i18n.choice_lang(), reply_markup=build_lang_kb())
        return

    await message.answer(i18n.your_profile_look())
    await message.answer_media_group(build_profile(profile).build())
    await show_menu(
        message=message,
        i18n=i18n,
    )


@router.message(F.text.in_(languages_text), StateFilter(None))
async def choice_language_handler(
    message: Message,
    i18n: I18nContext,
    user_repository: FromDishka[UserRepository],
) -> None:

    lang = resolve_lang(message.text)
    await i18n.set_locale(lang)

    state = UpdateUserState(
        update=UpdateUserDTO(tid=message.from_user.id, language=lang)
    )
    update_case = UpdateUserCase(user_repository=user_repository)
    await update_case(state)
    await message.answer(
        i18n.hello_text(), reply_markup=build_reply_keyboard(i18n.lets_go())
    )
