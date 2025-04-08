from pydantic import BaseModel, Field
from datetime import datetime

class SensorData(BaseModel):
    timestamp: datetime
    device_id: str
    heart_rate: int = Field(..., gt=30, lt=200)
    blood_pressure: str  # format "120/80"
    glucose_level: float = Field(..., gt=40, lt=400)
    oxygen_saturation: float = Field(..., gt=50, lt=100)
