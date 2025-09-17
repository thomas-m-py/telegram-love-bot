from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, status

from src.bot import main_bot
from src.bot.app import dp
from src.bot.webhook_utils import create_secret_token
from src.settings.secrets import secrets


sec_token = create_secret_token(secrets.MAIN_BOT_TOKEN, secrets.SECRET_TOKEN)


@asynccontextmanager
async def lifespan(app_: FastAPI):

    await dp.emit_startup(
        **{
            "dispatcher": dp,
            **dp.workflow_data,
        }
    )
    yield
    await dp.emit_shutdown(
        **{
            "dispatcher": dp,
            **dp.workflow_data,
        }
    )

    await main_bot.session.close()


app = FastAPI(
    lifespan=lifespan,
)


@app.post("/webhook/", include_in_schema=False)
async def telegram_post(request: Request) -> Response:
    data = await request.json()
    token = request.headers.get("x-telegram-bot-api-secret-token")
    if token != sec_token:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    await dp.feed_webhook_update(main_bot, data)
    return Response(status_code=status.HTTP_202_ACCEPTED)
