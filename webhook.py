import logging

from aiogram import Bot
from aiohttp import web
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from app import create_dispatcher, create_bot

log = logging.getLogger(__name__)

LOCAL_WEBAPP_HOST = "0.0.0.0"
LOCAL_WEBAPP_PORT = 8080

WEBHOOK_PATH = "/bots/webhook"
# WEBHOOK_SECRET_TOKEN = ""

# set your public url!
WEBHOOK_BASE_URL = ""


async def on_bot_startup(bot: Bot) -> None:
    me = await bot.get_me()
    log.warning("Starting bot %s", me.username)
    # TODO: get webhook info, compare with target url, delete + set only if different
    await bot.delete_webhook(drop_pending_updates=False)

    url = f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(url=url)

    wh_info = await bot.get_webhook_info()
    log.info("Successfully set webhook %s", wh_info)


def create_prepared_web_app() -> web.Application:
    bot = create_bot()
    dp = create_dispatcher()
    dp.startup.register(on_bot_startup)

    app = web.Application()

    aiogram_webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        # secret_token=WEBHOOK_SECRET_TOKEN,
        handle_in_background=False,
    )
    aiogram_webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    return app


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app = create_prepared_web_app()

    web.run_app(
        app,
        host=LOCAL_WEBAPP_HOST,
        port=LOCAL_WEBAPP_PORT,
    )


if __name__ == "__main__":
    main()
