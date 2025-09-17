__all__ = ("main",)

from gunicorn_app import Application
from options import get_app_options
from src.bot.web import app


def main():
    Application(
        application=app,
        options=get_app_options(
            host="0.0.0.0",
            port=8000,
            timeout=180,
            workers=4,
            log_level="info",
        ),
    ).run()


if __name__ == "__main__":
    main()
