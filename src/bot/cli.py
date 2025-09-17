import argparse
import asyncio

from src.bot import main_bot
from src.bot.webhook_utils import create_secret_token
from src.settings.secrets import secrets


async def cmd_set(url: str | None) -> None:
    current_url = (await main_bot.get_webhook_info()).url
    if url is None:
        webhook_url = secrets.WEBHOOK_HOST.rstrip("/") + "/webhook/"
    else:
        webhook_url = url
    sec = create_secret_token(secrets.MAIN_BOT_TOKEN, secrets.SECRET_TOKEN)
    if current_url != webhook_url:
        await main_bot.set_webhook(url=webhook_url, secret_token=sec)

    await main_bot.session.close()


async def cmd_delete() -> None:
    await main_bot.delete_webhook(drop_pending_updates=False)
    await main_bot.session.close()


async def cmd_info() -> None:
    info = await main_bot.get_webhook_info()
    await main_bot.session.close()
    print(info)


def main() -> None:
    parser = argparse.ArgumentParser(prog="telegram-webhook")
    sub = parser.add_subparsers(dest="command", required=True)

    set_cmd = sub.add_parser("set", help="Set webhook URL")
    set_cmd.add_argument(
        "--url", required=False, help="Webhook URL (default from settings)"
    )

    sub.add_parser("delete", help="Delete webhook")
    sub.add_parser("info", help="Show webhook info")

    args = parser.parse_args()

    if args.command == "set":
        asyncio.run(cmd_set(args.url))
        return
    if args.command == "delete":
        asyncio.run(cmd_delete())
        return
    if args.command == "info":
        asyncio.run(cmd_info())
        return


if __name__ == "__main__":
    main()
