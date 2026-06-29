import asyncio
from typing import AsyncIterator, Dict
from core.interfaces import EventBus
from pydantic import BaseModel

class InMemoryEventBus(EventBus):
    def __init__(self):
        self._queues: Dict[str, asyncio.Queue] = {}

    def _get_queue(self, topic: str) -> asyncio.Queue:
        if topic not in self._queues:
            self._queues[topic] = asyncio.Queue()
        return self._queues[topic]

    async def publish(self, topic: str, event: BaseModel):
        await self._get_queue(topic).put(event)

    async def subscribe(self, topic: str) -> AsyncIterator[BaseModel]:
        queue = self._get_queue(topic)
        while True:
            event = await queue.get()
            yield event
