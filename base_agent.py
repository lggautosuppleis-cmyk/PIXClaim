import abc
import asyncio
import json
from typing import List
import aioredis

from src.utils.logger import get_logger

logger = get_logger("agent.base")

class BaseAgent(abc.ABC):
    def __init__(self, name: str, redis_url: str):
        self.name = name
        self.redis_url = redis_url
        self.redis = None
        self.running = False

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
        logger.info({"agent": self.name, "action": "connected_redis"})

    @abc.abstractmethod
    async def start(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def handle_message(self, channel: str, message: dict):
        raise NotImplementedError

    async def publish(self, channel: str, message: dict):
        try:
            await self.redis.publish(channel, json.dumps(message))
            logger.debug({"agent": self.name, "action": "publish", "channel": channel, "message": message})
        except Exception as e:
            logger.exception({"agent": self.name, "action": "publish_failed", "error": str(e)})

    async def _listen(self, channels: List[str]):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(*channels)
        logger.info({"agent": self.name, "action": "subscribed", "channels": channels})
        async for raw in pubsub.listen():
            if raw is None or raw.get("type") != "message":
                continue
            try:
                ch = raw.get("channel")
                data = json.loads(raw.get("data"))
                await self.handle_message(ch, data)
            except Exception as e:
                logger.exception({"agent": self.name, "action": "handle_message_error", "error": str(e)})

    async def _heartbeat_loop(self, interval: int = 30):
        while self.running:
            await self.publish("conductor:events", {"event": "heartbeat", "agent": self.name})
            await asyncio.sleep(interval)

    async def run(self, channels: List[str] = []):
        await self.connect()
        self.running = True
        tasks = []
        if channels:
            tasks.append(asyncio.create_task(self._listen(channels)))
        tasks.append(asyncio.create_task(self._heartbeat_loop()))
        await asyncio.gather(*tasks)
