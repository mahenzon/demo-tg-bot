import asyncio
from collections import defaultdict
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types

DataType = dict[str, Any]
AlbumMessages = list[types.Message]


class AlbumMiddleware(BaseMiddleware):
    def __init__(self, timeout: float = 0.1):
        self.timeout = timeout
        self.album_messages = defaultdict[str, AlbumMessages](list)

    def get_count(self, message: types.Message) -> int:
        return len(self.album_messages[message.media_group_id])

    def store_album_message(self, message: types.Message) -> int:
        self.album_messages[message.media_group_id].append(message)
        return self.get_count(message)

    def get_result_album(self, message: types.Message) -> AlbumMessages:
        album_messages = self.album_messages.pop(message.media_group_id)
        album_messages.sort(key=lambda m: m.message_id)
        return album_messages

    async def __call__[T](
        self,
        handler: Callable[[types.Message, DataType], Awaitable[T]],
        event: types.Message,
        data: DataType,
    ) -> T | None:
        if event.media_group_id is None:
            return await handler(event, data)

        count = self.store_album_message(event)
        # ждём обработку других сообщений из группы
        await asyncio.sleep(self.timeout)
        # проверяем, были ли ещё сообщения из группы добавлены.
        # если нет (не поменялось количеств),
        # то тут мы обработали последнее сообщение.
        # можно отдавать его в обработчик.
        new_count = self.get_count(event)
        if new_count != count:
            return None

        data.update(
            album_messages=self.get_result_album(event),
        )
        return await handler(event, data)
