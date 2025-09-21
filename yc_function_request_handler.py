import base64
import io
import logging
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from aiogram.methods import TelegramMethod
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import Payload

if TYPE_CHECKING:
    from typing import TypedDict

    class EventType(TypedDict):
        body: str
        headers: dict[str, str]


log = logging.getLogger(__name__)


class AsyncBytesIO:
    def __init__(self):
        self.buffer = io.BytesIO()

    async def write(self, data) -> None:
        self.buffer.write(data)

    def getvalue(self) -> bytes:
        return self.buffer.getvalue()


async def prepare_response_base64(writer: Payload) -> str:
    buffer = AsyncBytesIO()

    # noinspection PyTypeChecker
    await writer.write(buffer)

    base64_encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return base64_encoded


class YCRequestHandler(SimpleRequestHandler):
    DEFAULT_STATUS_CODE = 200
    SECRET_TOKEN_HEADER = "X-Telegram-Bot-Api-Secret-Token"

    async def handle_raw_event(
        self,
        json_string: str,
    ) -> TelegramMethod[Any] | None:
        try:
            return await self.dispatcher.feed_update(
                bot=self.bot,
                update=Update.model_validate_json(json_string),
                **self.data,
            )
        except Exception:
            log.exception(
                "Unhandled exception during feeding data %r",
                json_string,
            )

    async def handle_yc_function_request(
        self,
        event: "EventType",
    ):
        secret_token = event["headers"].get(self.SECRET_TOKEN_HEADER) or ""

        if not self.verify_secret(secret_token, self.bot):
            return {
                "statusCode": HTTPStatus.UNAUTHORIZED,
                "headers": {"Content-Type": "text/plain"},
                "isBase64Encoded": False,
                "body": "Unauthorized",
            }

        result = await self.handle_raw_event(event["body"])
        response_writer = self._build_response_writer(
            bot=self.bot,
            result=result,
        )
        response_body = await prepare_response_base64(response_writer)
        return {
            "statusCode": self.DEFAULT_STATUS_CODE,
            "headers": dict(response_writer.headers.items()),
            "isBase64Encoded": True,
            "body": response_body,
        }
