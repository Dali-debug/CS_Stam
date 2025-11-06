"""
Processed Health Metrics model for MongoDB
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import os

class CardiovascularMetrics(BaseModel):
    avg_heart_rate_bpm: float = Field(..., ge=30, le=250)
    min_heart_rate_bpm: int = Field(..., ge=30, le=250)
    max_heart_rate_bpm: int = Field(..., ge=30, le=250)
    resting_heart_rate_bpm: Optional[int] = Field(None, ge=30, le=120)
    avg_hrv_ms: float = Field(..., ge=0, le=500)
    avg_spo2_percent: float = Field(..., ge=70, le=100)

class ActivityMetrics(BaseModel):
    steps_count: int = Field(..., ge=0)
    distance_meters: float = Field(..., ge=0)
    calories_burned: int = Field(..., ge=0)
    active_minutes: int = Field(..., ge=0, le=1440)
    sedentary_minutes: int = Field(..., ge=0, le=1440)
    intensity_level: str = Field(..., pattern=r'^(low|moderate|high)$')

class StressMetrics(BaseModel):
    avg_stress_level: float = Field(..., ge=0, le=10)
    stress_duration_minutes: int = Field(..., ge=0, le=1440)
    relaxation_score: float = Field(..., ge=0, le=100)

class SleepMetrics(BaseModel):
    is_sleeping: bool
    sleep_stage: Optional[str] = Field(None, pattern=r'^(awake|light|deep|rem)$')
    sleep_quality_score: Optional[float] = Field(None, ge=0, le=100)

class ProcessedHealthMetricsModel(BaseModel):
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    cardiovascular: CardiovascularMetrics
    activity: ActivityMetrics
    stress: StressMetrics
    sleep: SleepMetrics
    avg_skin_temperature_celsius: float = Field(..., ge=20, le=45)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": "2025-11-05T11:00:00Z",
                "cardiovascular": {
                    "avg_heart_rate_bpm": 72.5,
                    "min_heart_rate_bpm": 60,
                    "max_heart_rate_bpm": 95,
                    "resting_heart_rate_bpm": 62,
                    "avg_hrv_ms": 48.2,
                    "avg_spo2_percent": 97.8
                },
                "activity": {
                    "steps_count": 1250,
                    "distance_meters": 875.5,
                    "calories_burned": 95,
                    "active_minutes": 45,
                    "sedentary_minutes": 15,
                    "intensity_level": "moderate"
                },
                "stress": {
                    "avg_stress_level": 3.5,
                    "stress_duration_minutes": 20,
                    "relaxation_score": 75.0
                },
                "sleep": {
                    "is_sleeping": False,
                    "sleep_stage": None,
                    "sleep_quality_score": None
                },
                "avg_skin_temperature_celsius": 36.2
            }
        }

# MongoDB collection name
COLLECTION_NAME = "processedHealthMetrics"

# TTL in seconds (30 days)
TTL_SECONDS = int(os.getenv('PROCESSED_METRICS_TTL', '30')) * 24 * 60 * 60

# Indexes to be created
INDEXES = [
    {"keys": [("user_id", 1), ("timestamp", -1)]},
    {"keys": [("timestamp", -1)]},
    {"keys": [("timestamp", 1)], "options": {"expireAfterSeconds": TTL_SECONDS}},
]
