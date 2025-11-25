"""
External service for demonstrating credential usage
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, Any


class ExternalService:
    """Mock external service for demonstrating various API integrations"""

    def __init__(self, credentials: Dict[str, Any]):
        if not credentials:
            raise ValueError("No credentials provided for ExternalService")
        self.credentials = credentials

    async def fetch_weather_data(self, city: str) -> Dict[str, Any]:
        """Mock weather API call"""
        await asyncio.sleep(0.1)

        return {
            "city": city,
            "temperature": random.uniform(-10, 35),
            "humidity": random.uniform(30, 90),
            "conditions": random.choice(["sunny", "cloudy", "rainy", "snowy"]),
            "timestamp": datetime.now().isoformat(),
        }

    async def send_notification(self, message: str, recipient: str) -> Dict[str, Any]:
        """Mock notification service"""
        await asyncio.sleep(0.05)

        return {
            "message_id": f"msg_{random.randint(1000, 9999)}",
            "recipient": recipient,
            "status": "sent",
            "sent_at": datetime.now().isoformat(),
        }

    async def process_payment(
        self, amount: float, currency: str = "USD"
    ) -> Dict[str, Any]:
        """Mock payment processing"""
        await asyncio.sleep(0.3)  # Simulate payment gateway latency

        success = random.random() > 0.1  # 90% success rate

        return {
            "transaction_id": f"txn_{random.randint(10000, 99999)}",
            "amount": amount,
            "currency": currency,
            "status": "completed" if success else "failed",
            "processed_at": datetime.now().isoformat(),
        }
