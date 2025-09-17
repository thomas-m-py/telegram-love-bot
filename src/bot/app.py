from pathlib import Path

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from dishka.integrations.aiogram import setup_dishka

from src.bot.handlers.start import router as start_router
from src.bot.handlers.create_update_profile import (
    router as create_update_profile_router,
)
from src.bot.handlers.find_profile import router as find_profile_router
from src.bot.handlers.my_profile import router as my_profile_router
from src.bot.handlers.show_matches import router as show_matches_router
from src.bot.handlers.disable_profile import router as disable_profile_router
from src.bot.middlewares.user_language_middleware import UserLanguageMiddleware
from src.bot.middlewares.user_middleware import UserMiddleware
from src.di_container import di_container
from src.settings.secrets import secrets

storage = RedisStorage.from_url(secrets.REDIS_URL)
dp = Dispatcher(storage=storage)

dp.include_router(start_router)
dp.include_router(create_update_profile_router)
dp.include_router(find_profile_router)
dp.include_router(my_profile_router)
dp.include_router(show_matches_router)
dp.include_router(disable_profile_router)

path_dir_root = Path(__file__).parent.parent.parent.absolute() / "locales"

mw = I18nMiddleware(
    core=FluentRuntimeCore(
        path=path_dir_root,
    ),
    default_locale="ru",
)
mw.setup(dispatcher=dp)
dp.update.middleware(UserMiddleware())
dp.update.middleware(UserLanguageMiddleware(mw))

setup_dishka(container=di_container, router=dp, auto_inject=True)
