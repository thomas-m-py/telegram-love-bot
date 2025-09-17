from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def build_reply_keyboard(*button_texts: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for text in button_texts:
        builder.button(text=text)
    return builder.as_markup(resize_keyboard=True)
