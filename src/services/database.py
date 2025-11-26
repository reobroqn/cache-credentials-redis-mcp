"""
Database service for demonstrating credential usage
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, Any, List


class DatabaseService:
    """Mock database service that simulates database operations"""

    def __init__(self, credentials: Dict[str, Any]):
        if not credentials:
            raise ValueError("No credentials provided for DatabaseService")
        self.credentials = credentials

    async def query_users(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Mock database query to fetch users"""
        await asyncio.sleep(0.1)  # Simulate database query time

        users = []
        for i in range(min(limit, 50)):
            users.append(
                {
                    "id": f"user_{i + 1}",
                    "name": f"User {i + 1}",
                    "email": f"user{i + 1}@example.com",
                    "role": random.choice(["admin", "user", "viewer"]),
                    "created_at": datetime.now().isoformat(),
                }
            )

        return users

    async def get_analytics_data(self, days: int = 7) -> Dict[str, Any]:
        """Mock database query for analytics data"""
        await asyncio.sleep(0.2)

        return {
            "period_days": days,
            "total_users": random.randint(100, 1000),
            "active_users": random.randint(50, 500),
            "new_signups": random.randint(5, 50),
            "revenue": random.uniform(1000, 10000),
            "generated_at": datetime.now().isoformat(),
        }
