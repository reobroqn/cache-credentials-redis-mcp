"""
API service for demonstrating credential usage
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, Any


class APIService:
    """Mock API service that simulates external API calls with authentication"""

    def __init__(self, credentials: Dict[str, Any]):
        if not credentials:
            raise ValueError("No credentials provided for APIService")
        self.credentials = credentials

    async def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Mock API call to get user data"""
        await asyncio.sleep(0.1)  # Simulate network latency

        return {
            "user_id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com",
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
            "status": "active",
        }

    async def fetch_metrics(self, metric_type: str = "performance") -> Dict[str, Any]:
        """Mock API call to fetch system metrics"""
        await asyncio.sleep(0.2)

        return {
            "metric_type": metric_type,
            "timestamp": datetime.now().isoformat(),
            "cpu_usage": random.uniform(10, 90),
            "memory_usage": random.uniform(20, 80),
            "disk_usage": random.uniform(30, 70),
            "network_io": random.uniform(100, 1000),
        }
