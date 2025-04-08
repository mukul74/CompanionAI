from agents.sensor_agent import SensorAgent
from agents.health_monitor_agent import HealthMonitoringAgent
from datetime import datetime

sensor_data = {
    "timestamp": datetime.now().isoformat(),
    "device_id": "elderly_device_001",
    "heart_rate": 52,
    "blood_pressure": "150/95",
    "glucose_level": 190.0,
    "oxygen_saturation": 89.0
}

validated = SensorAgent().run(sensor_data)
report = HealthMonitoringAgent().run(validated)

print("\nTool Assessment:\n", report["tool_assessment"])
print("\nLLM Analysis:\n", report["llm_analysis"])
