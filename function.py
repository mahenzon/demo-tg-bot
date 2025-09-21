from app import create_dispatcher, create_bot
from config import settings
from yc_function_request_handler import YCRequestHandler

dp = create_dispatcher()
bot = create_bot()

request_handler = YCRequestHandler(
    dispatcher=dp,
    bot=bot,
    handle_in_background=False,
    secret_token=settings.webhook_secret_token,
)


async def handler(event, context):
    return await request_handler.handle_yc_function_request(event)
