"""
Database configuration and connection management for MongoDB using Motor (async driver)
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from loguru import logger
from typing import Optional
import asyncio

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db = None
    
    @classmethod
    async def connect(cls):
        """Connect to MongoDB with retry logic"""
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = os.getenv('MONGODB_DB_NAME', 'healthcare')
        max_retries = 5
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to connect to MongoDB (attempt {attempt + 1}/{max_retries})...")
                
                cls.client = AsyncIOMotorClient(
                    mongodb_uri,
                    maxPoolSize=10,
                    minPoolSize=2,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=10000,
                    socketTimeoutMS=10000
                )
                
                # Test connection
                await cls.client.admin.command('ping')
                
                cls.db = cls.client[db_name]
                
                logger.info(f"✅ Successfully connected to MongoDB database: {db_name}")
                return
                
            except (ConnectionFailure, ServerSelectionTimeoutError) as error:
                logger.error(f"❌ MongoDB connection failed (attempt {attempt + 1}/{max_retries}): {error}")
                
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.critical("Failed to connect to MongoDB after maximum retries")
                    raise
    
    @classmethod
    async def disconnect(cls):
        """Disconnect from MongoDB"""
        if cls.client:
            cls.client.close()
            logger.info("Disconnected from MongoDB")
    
    @classmethod
    async def get_stats(cls):
        """Get database statistics"""
        if not cls.db:
            return None
        
        stats = await cls.db.command('dbStats')
        return {
            'database': stats.get('db'),
            'collections': stats.get('collections'),
            'dataSize': stats.get('dataSize'),
            'indexSize': stats.get('indexSize'),
            'storageSize': stats.get('storageSize')
        }
    
    @classmethod
    def is_connected(cls) -> bool:
        """Check if connected to MongoDB"""
        return cls.client is not None

# Global database instance
db_instance = Database()
