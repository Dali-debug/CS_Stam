"""
Raw Sensor Data model for MongoDB
"""
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field
import os

class PPGData(BaseModel):
    heart_rate_bpm: int = Field(..., ge=30, le=250)
    hrv_ms: float = Field(..., ge=0, le=500)
    spo2_percent: int = Field(..., ge=70, le=100)
    signal_quality: float = Field(..., ge=0, le=1)

class IMUData(BaseModel):
    accelerometer_x: float = Field(..., ge=-20, le=20)
    accelerometer_y: float = Field(..., ge=-20, le=20)
    accelerometer_z: float = Field(..., ge=-20, le=20)
    gyroscope_x: float = Field(..., ge=-500, le=500)
    gyroscope_y: float = Field(..., ge=-500, le=500)
    gyroscope_z: float = Field(..., ge=-500, le=500)

class RawSensorDataModel(BaseModel):
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ppg: PPGData
    imu: IMUData
    skin_temperature_celsius: float = Field(..., ge=20, le=45)
    eda_microsiemens: float = Field(..., ge=0, le=100)
    battery_level_percent: int = Field(..., ge=0, le=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": "2025-11-05T10:30:00Z",
                "ppg": {
                    "heart_rate_bpm": 75,
                    "hrv_ms": 45.5,
                    "spo2_percent": 98,
                    "signal_quality": 0.95
                },
                "imu": {
                    "accelerometer_x": 0.5,
                    "accelerometer_y": -0.2,
                    "accelerometer_z": 9.8,
                    "gyroscope_x": 0.0,
                    "gyroscope_y": 0.0,
                    "gyroscope_z": 0.0
                },
                "skin_temperature_celsius": 36.5,
                "eda_microsiemens": 2.5,
                "battery_level_percent": 85
            }
        }

# MongoDB collection name
COLLECTION_NAME = "rawSensorData"

# TTL in seconds (7 days)
TTL_SECONDS = int(os.getenv('RAW_SENSOR_TTL', '7')) * 24 * 60 * 60

# Indexes to be created
INDEXES = [
    {"keys": [("user_id", 1), ("timestamp", -1)]},
    {"keys": [("timestamp", -1)]},
    {"keys": [("timestamp", 1)], "options": {"expireAfterSeconds": TTL_SECONDS}},
]
