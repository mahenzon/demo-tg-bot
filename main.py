import asyncio
import logging
from app import create_dispatcher, create_bot


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = create_dispatcher()

    bot = create_bot()
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
