from pydantic import BaseModel
from typing import Any, Dict

class BaseState(BaseModel):
    input: Dict[str, Any]
    sensor_data: Dict[str, Any] = None
    health_report: Dict[str, Any] = None
    alert: Dict[str, Any] = None
