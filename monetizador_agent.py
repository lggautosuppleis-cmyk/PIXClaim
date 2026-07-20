import asyncio
from src.agents.base_agent import BaseAgent
from src.services.payments.stripe_service import StripeService
from src.utils.logger import get_logger

logger = get_logger("agent.monetizador")

class Monetizador(BaseAgent):
    def __init__(self, redis_url: str, stripe_api_key: str):
        super().__init__("monetizador", redis_url)
        self.stripe = StripeService(stripe_api_key)

    async def start(self):
        await self.run(channels=["business:estimates", "conductor:control"])

    async def handle_message(self, channel: str, message: dict):
        event = message.get("event")
        if event == "estimate.completed":
            await self.handle_estimate_completed(message)
        elif event == "conductor.command":
            logger.info({"received": message})

    async def handle_estimate_completed(self, payload: dict):
        base = payload.get("amount", 0.0)
        take_rate = 0.02
        fee = round(base * take_rate, 2)
        customer_id = payload.get("metadata", {}).get("customer_id")
        if not customer_id:
            await self.publish("payments:events", {"event": "payment.failed", "estimate": payload.get("id"), "reason": "no_customer"})
            return
        try:
            resp = self.stripe.create_charge(customer_id, fee, currency="usd", metadata={"estimate": payload.get("id")})
            await self.publish("payments:events", {"event": "payment.succeeded", "estimate": payload.get("id"), "amount": fee})
            logger.info({"agent": self.name, "action": "charged", "amount": fee, "customer": customer_id})
        except Exception as e:
            logger.exception({"agent": self.name, "action": "charge_failed", "error": str(e)})
            await self.publish("payments:events", {"event": "payment.failed", "estimate": payload.get("id"), "reason": str(e)})
