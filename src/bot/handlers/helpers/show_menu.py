from aiogram.types import Message
from aiogram_i18n import I18nContext

from src.bot.utils.keyboard import build_reply_keyboard


async def show_menu(
    message: Message,
    i18n: I18nContext,
):
    keyboard_menu = build_reply_keyboard(
        i18n.menu_start_find_profiles_button_text(),
        i18n.menu_my_profile_button_text(),
        i18n.menu_disable_my_profile_button_text(),
    )
    await message.answer(i18n.main_menu(), reply_markup=keyboard_menu)
