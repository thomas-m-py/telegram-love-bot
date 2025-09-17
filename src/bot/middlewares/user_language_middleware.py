from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_i18n import I18nMiddleware, I18nContext


class UserLanguageMiddleware(BaseMiddleware):
    def __init__(self, i18n_middleware: I18nMiddleware):
        self.i18n_middleware = i18n_middleware

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("user")
        user_language = user.language
        i18n: I18nContext = data.get("i18n")
        if user_language == i18n.locale:
            return await handler(event, data)

        if user_language in self.i18n_middleware.core.available_locales:
            await i18n.set_locale(user_language)
        return await handler(event, data)
