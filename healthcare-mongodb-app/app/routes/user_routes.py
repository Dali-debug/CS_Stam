"""
User routes for FastAPI
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models.user import UserModel
from app.services.user_service import UserService
from loguru import logger

router = APIRouter()
user_service = UserService()

@router.post("/users", status_code=201)
async def create_user(user: UserModel):
    """Create a new user"""
    try:
        result = await user_service.create_user(user.dict())
        return {
            "message": "User created successfully",
            "user_id": result
        }
    except Exception as error:
        logger.error(f"Error creating user: {error}")
        raise HTTPException(status_code=400, detail=str(error))

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user by ID"""
    try:
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error getting user: {error}")
        raise HTTPException(status_code=500, detail=str(error))

@router.get("/users")
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None
):
    """Get all users with pagination"""
    try:
        result = await user_service.get_all_users(page, limit, is_active)
        return result
    except Exception as error:
        logger.error(f"Error getting users: {error}")
        raise HTTPException(status_code=500, detail=str(error))

@router.put("/users/{user_id}/profile")
async def update_profile(user_id: str, profile_data: dict):
    """Update user profile"""
    try:
        result = await user_service.update_profile(user_id, profile_data)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "Profile updated successfully"}
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error updating profile: {error}")
        raise HTTPException(status_code=400, detail=str(error))

@router.put("/users/{user_id}/goal")
async def update_goal(user_id: str, goal_data: dict):
    """Update user goal"""
    try:
        result = await user_service.update_goal(user_id, goal_data)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "Goal updated successfully"}
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error updating goal: {error}")
        raise HTTPException(status_code=400, detail=str(error))

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Soft delete user"""
    try:
        result = await user_service.delete_user(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as error:
        logger.error(f"Error deleting user: {error}")
        raise HTTPException(status_code=500, detail=str(error))
