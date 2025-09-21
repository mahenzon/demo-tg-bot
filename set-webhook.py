import asyncio
import logging

from app import create_bot
from config import settings


WEBHOOK_URL = (
    "https://d5de6eogclq3hj8luksj.8wihnuyr.apigw.yandexcloud.net/demo-bot-webhook"
)

log = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = create_bot()
    log.warning("Me: %s", await bot.get_me())
    log.info("Webhook info: %s", await bot.get_webhook_info())

    log.warning("Deleting webhook")
    await bot.delete_webhook()
    log.info("Webhook deleted, set new webhook url %r", WEBHOOK_URL)
    await bot.set_webhook(
        WEBHOOK_URL,
        allowed_updates=[
            "message",
            "callback_query",
            "poll",
        ],
        secret_token=settings.webhook_secret_token,
        # drop_pending_updates=True,
    )
    log.info("Successfully set new webhook %r", await bot.get_webhook_info())


if __name__ == "__main__":
    asyncio.run(main())
