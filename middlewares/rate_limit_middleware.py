import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types

from utils.async_timed_queue import AsyncTimedQueue


log = logging.getLogger(__name__)


@dataclass
class RateLimitInfo:
    message_count: int
    first_message: datetime | None


class RateLimitMiddleware(BaseMiddleware):

    def __init__(
        self,
        rate_limit: int = 5,
        time_interval: timedelta = timedelta(seconds=30),
    ):
        self.rate_limit = rate_limit
        self.processed_messages_ts = defaultdict[int, AsyncTimedQueue[datetime]](
            lambda: AsyncTimedQueue(max_age=time_interval)
        )

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: dict[str, Any],
    ) -> Any:

        user_id = event.from_user.id
        current_dt = datetime.now()
        processed_messages = self.processed_messages_ts[user_id]
        count: int = await processed_messages.get_len()

        if count > self.rate_limit:
            log.info("Skip user %s message", user_id)
            return

        await processed_messages.put(current_dt)
        count = await processed_messages.get_len()
        if count > self.rate_limit:
            log.info("Skip user %s message (new)", user_id)
            return
        if count == self.rate_limit:
            log.info(
                "Sending last message to user %s before rate limit",
                user_id,
            )
            await event.reply(
                text="You're sending too many messages. Please cool down for some time",
            )
            return

        data.update(
            rate_limit_info=RateLimitInfo(
                message_count=count,
                first_message=await processed_messages.peek(),
            ),
        )

        return await handler(event, data)
