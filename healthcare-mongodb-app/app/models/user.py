"""
User model for MongoDB
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"

class HealthGoal(str, Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    IMPROVE_FITNESS = "improve_fitness"
    STRESS_MANAGEMENT = "stress_management"
    BETTER_SLEEP = "better_sleep"
    GENERAL_HEALTH = "general_health"

class Profile(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: datetime
    gender: Gender
    height_cm: float = Field(..., gt=0, le=300)
    weight_kg: float = Field(..., gt=0, le=500)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')

class MedicalInfo(BaseModel):
    blood_type: Optional[str] = Field(None, pattern=r'^(A|B|AB|O)[+-]$')
    chronic_conditions: List[str] = []
    medications: List[str] = []
    allergies: List[str] = []
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class Goal(BaseModel):
    type: HealthGoal
    target_weight_kg: Optional[float] = Field(None, gt=0, le=500)
    target_steps_per_day: Optional[int] = Field(None, ge=0, le=100000)
    target_sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    target_calories_per_day: Optional[int] = Field(None, ge=0, le=10000)
    activity_level: ActivityLevel

class DeviceInfo(BaseModel):
    device_id: str
    device_model: str
    firmware_version: str
    last_sync: datetime = Field(default_factory=datetime.utcnow)

class UserModel(BaseModel):
    user_id: str = Field(..., description="Unique user identifier (UUID)")
    profile: Profile
    medical_info: Optional[MedicalInfo] = None
    goal: Optional[Goal] = None
    device_info: Optional[DeviceInfo] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    is_deleted: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "profile": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "date_of_birth": "1990-01-01T00:00:00Z",
                    "gender": "male",
                    "height_cm": 175.5,
                    "weight_kg": 75.0,
                    "email": "john.doe@example.com",
                    "phone": "+1234567890"
                },
                "medical_info": {
                    "blood_type": "O+",
                    "chronic_conditions": ["hypertension"],
                    "medications": ["lisinopril"],
                    "allergies": [],
                    "emergency_contact_name": "Jane Doe",
                    "emergency_contact_phone": "+1234567891"
                },
                "goal": {
                    "type": "weight_loss",
                    "target_weight_kg": 70.0,
                    "target_steps_per_day": 10000,
                    "target_sleep_hours": 8.0,
                    "activity_level": "moderately_active"
                }
            }
        }

# MongoDB collection name
COLLECTION_NAME = "users"

# Indexes to be created
INDEXES = [
    {"keys": [("user_id", 1)], "options": {"unique": True}},
    {"keys": [("profile.email", 1)], "options": {"unique": True}},
    {"keys": [("is_deleted", 1)]},
    {"keys": [("created_at", -1)]},
    {"keys": [("device_info.device_id", 1)]},
]
