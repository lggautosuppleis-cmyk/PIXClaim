import os
import aioredis
import json

REDIS_URL = os.getenv("REDIS_URL","redis://localhost:6379/0")

async def publish_event(channel: str, payload: dict):
    r = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    await r.publish(channel, json.dumps(payload))
    await r.close()
