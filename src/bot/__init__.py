from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode

from src.settings.secrets import secrets

session = None
if secrets.ENABLE_LOCAL_BOTAPI:
    session = AiohttpSession(api=TelegramAPIServer.from_base(secrets.LOCAL_BOTAPI_URL))

main_bot = Bot(
    token=secrets.MAIN_BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
