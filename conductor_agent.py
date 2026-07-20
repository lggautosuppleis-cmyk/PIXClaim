from src.agents.base_agent import BaseAgent
from src.utils.logger import get_logger

logger = get_logger("agent.conductor")

class Conductor(BaseAgent):
    def __init__(self, redis_url: str):
        super().__init__("conductor", redis_url)

    async def start(self):
        await self.run(channels=["conductor:control"])

    async def handle_message(self, channel: str, message: dict):
        cmd = message.get("cmd")
        if cmd == "deploy.service":
            await self.publish("infra:ops", {"event": "deploy", "service": message.get("service"), "version": message.get("version"), "request_id": message.get("request_id")})
            logger.info({"agent": self.name, "action": "forward_deploy", "service": message.get("service")})
        else:
            logger.info({"agent": self.name, "action": "unknown_command", "payload": message})
