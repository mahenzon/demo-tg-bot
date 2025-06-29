import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties

from aiogram.enums import ParseMode

from config import settings
from middlewares.rate_limit_middleware import RateLimitMiddleware
from routers import router as main_router


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.message.middleware(RateLimitMiddleware(rate_limit=10))

    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
