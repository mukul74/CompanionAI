from typing import Any
from pydantic import BaseModel

class BaseState(BaseModel):
    input: Any = None
    sensor_data: Any = None
    health_report: Any = None
    alert_result: Any = None
    reminder: Any = None
