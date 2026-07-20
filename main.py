# Entrypoint dispatcher: arranca el proceso segun ROLE
# Roles: api | conductor | monetizador | operaciones | connectors
import os
import asyncio
import subprocess
import sys

from src.utils.logger import get_logger

logger = get_logger("main")

ROLE = os.getenv("ROLE", "api")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")


def run_api():
    logger.info({"action": "start", "role": "api"})
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "src.services.api.routes:app",
         "--host", "0.0.0.0", "--port", "8000"],
        check=True,
    )


async def run_conductor():
    from src.conductor.conductor_agent import Conductor
    agent = Conductor(REDIS_URL)
    await agent.start()


async def run_monetizador():
    from src.agents.monetizador_agent import Monetizador
    agent = Monetizador(REDIS_URL, STRIPE_API_KEY)
    await agent.start()


async def run_operaciones():
    from src.agents.base_agent import BaseAgent

    class Operaciones(BaseAgent):
        def __init__(self):
            super().__init__("operaciones", REDIS_URL)

        async def start(self):
            await self.run(channels=["infra:ops", "conductor:control"])

        async def handle_message(self, channel: str, message: dict):
            logger.info({"agent": self.name, "action": "received", "channel": channel, "message": message})
            if message.get("event") == "deploy":
                await self.publish("conductor:events", {
                    "event": "deploy.ack",
                    "service": message.get("service"),
                    "version": message.get("version"),
                    "request_id": message.get("request_id"),
                    "status": "accepted",
                })

    await Operaciones().start()


async def run_connectors():
    # Worker de ingesta: escucha solicitudes y ejecuta los conectores NHTSA
    import aioredis
    import json
    from src.connectors.nhtsa_vpic import ingest_vin
    from src.connectors.nhtsa_recalls import ingest_recalls_by_vin

    logger.info({"action": "start", "role": "connectors"})
    r = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("ingest:requests")
    logger.info({"action": "subscribed", "channels": ["ingest:requests"]})
    async for raw in pubsub.listen():
        if raw is None or raw.get("type") != "message":
            continue
        try:
            msg = json.loads(raw.get("data"))
            vin = msg.get("vin")
            if not vin:
                continue
            await ingest_vin(vin)
            await ingest_recalls_by_vin(vin)
            logger.info({"action": "ingested", "vin": vin})
        except Exception as e:
            logger.exception({"action": "ingest_error", "error": str(e)})


def main():
    if ROLE == "api":
        run_api()
    elif ROLE == "conductor":
        asyncio.run(run_conductor())
    elif ROLE == "monetizador":
        asyncio.run(run_monetizador())
    elif ROLE == "operaciones":
        asyncio.run(run_operaciones())
    elif ROLE == "connectors":
        asyncio.run(run_connectors())
    else:
        logger.error({"action": "unknown_role", "role": ROLE})
        sys.exit(1)


if __name__ == "__main__":
    main()
