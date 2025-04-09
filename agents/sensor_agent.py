from pydantic_ai.agent import Agent
from schemas.sensor_data import SensorData

class SensorAgent(Agent):
    name = "SensorAgent"
    description = "Collects and validates sensor data from devices."

    def run(self, data: dict) -> dict:
        print("[Sensor Agent] Validating sensor input...")
        sensor_data = SensorData(**data)
        print("[Sensor Agent] Validated sensor input")
        return sensor_data.dict()
