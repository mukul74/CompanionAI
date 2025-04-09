from pydantic_ai.agent import Agent
from schemas.sensor_data import SensorData
from rich.console import Console
class SensorAgent(Agent):
    name = "SensorAgent"
    description = "Collects and validates sensor data from devices."

    def run(self, data: dict) -> dict:
        console = Console()
        console.print("[bold blue][Sensor Agent][/bold blue] [yellow]Validating Input[/yellow]")
        sensor_data = SensorData(**data)
        console.print("[bold blue][Sensor Agent][/bold blue] [green]Validation Done[/green]")
        return sensor_data.dict()
