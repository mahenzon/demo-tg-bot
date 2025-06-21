import asyncio
from collections import deque
from datetime import timedelta, datetime


class AsyncTimedQueue[T: datetime]:
    def __init__(self, max_age: timedelta):
        self.max_age = max_age
        self.q = deque[T]()
        self._lock = asyncio.Lock()

    @classmethod
    def get_now(cls):
        return datetime.now()

    @classmethod
    def get_age(cls, item: T) -> datetime:
        return item

    async def clear_old(self):
        async with self._lock:
            current_time = self.get_now()
            while self.q and (current_time - self.get_age(self.q[0])) > self.max_age:
                self.q.popleft()

    async def put(self, item: T) -> None:
        await self.clear_old()
        async with self._lock:
            # async push
            self.q.append(item)

    async def peek(self) -> T | None:
        await self.clear_old()
        async with self._lock:
            # async get
            return self.q[0] if self.q else None

    async def get_len(self) -> int:
        await self.clear_old()
        return len(self.q)
