"""
MongoDB database connection and operations.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from ..config import settings

# Global database client
client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongodb():
    """Establish connection to MongoDB."""
    global client
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    print(f"Connected to MongoDB at {settings.MONGODB_URL}")


async def close_mongodb_connection():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")


def get_database():
    """Get database instance."""
    return client[settings.DATABASE_NAME]


def reports_collection():
    """Get the migration reports collection."""
    db = get_database()
    return db["migration_reports"]
