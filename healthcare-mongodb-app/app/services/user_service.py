"""
User service for database operations
"""
from datetime import datetime
from typing import Optional, Dict, Any
from app.config.database import db_instance
from app.models.user import COLLECTION_NAME, INDEXES
from loguru import logger

class UserService:
    def __init__(self):
        self.collection = None
    
    async def _get_collection(self):
        """Get users collection"""
        if not self.collection:
            self.collection = db_instance.db[COLLECTION_NAME]
            # Create indexes
            for index in INDEXES:
                await self.collection.create_index(
                    index["keys"],
                    **index.get("options", {})
                )
        return self.collection
    
    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user"""
        collection = await self._get_collection()
        
        # Check if user already exists
        existing = await collection.find_one({"user_id": user_data["user_id"]})
        if existing:
            raise ValueError("User with this ID already exists")
        
        # Check if email already exists
        existing_email = await collection.find_one({"profile.email": user_data["profile"]["email"]})
        if existing_email:
            raise ValueError("User with this email already exists")
        
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
        
        result = await collection.insert_one(user_data)
        logger.info(f"Created user: {user_data['user_id']}")
        
        return user_data["user_id"]
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        collection = await self._get_collection()
        user = await collection.find_one(
            {"user_id": user_id, "is_deleted": False},
            {"_id": 0}
        )
        return user
    
    async def get_all_users(
        self,
        page: int = 1,
        limit: int = 10,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Get all users with pagination"""
        collection = await self._get_collection()
        
        query = {"is_deleted": False}
        if is_active is not None:
            query["is_active"] = is_active
        
        skip = (page - 1) * limit
        
        cursor = collection.find(query, {"_id": 0}).skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        
        total = await collection.count_documents(query)
        
        return {
            "users": users,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }
    
    async def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Update user profile"""
        collection = await self._get_collection()
        
        update_data = {
            f"profile.{key}": value 
            for key, value in profile_data.items()
        }
        update_data["updated_at"] = datetime.utcnow()
        
        result = await collection.update_one(
            {"user_id": user_id, "is_deleted": False},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            logger.info(f"Updated profile for user: {user_id}")
        
        return result.modified_count > 0
    
    async def update_goal(self, user_id: str, goal_data: Dict[str, Any]) -> bool:
        """Update user goal"""
        collection = await self._get_collection()
        
        result = await collection.update_one(
            {"user_id": user_id, "is_deleted": False},
            {
                "$set": {
                    "goal": goal_data,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            logger.info(f"Updated goal for user: {user_id}")
        
        return result.modified_count > 0
    
    async def delete_user(self, user_id: str) -> bool:
        """Soft delete user"""
        collection = await self._get_collection()
        
        result = await collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_deleted": True,
                    "is_active": False,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            logger.info(f"Deleted user: {user_id}")
        
        return result.modified_count > 0
