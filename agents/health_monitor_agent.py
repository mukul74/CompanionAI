from pydantic_ai.agent import Agent
from langchain_community.llms import Ollama
from tools.access_tools import access_all_vitals

class HealthMonitoringAgent(Agent):
    name = "HealthMonitoringAgent"
    description = "Analyzes sensor data and provides health insights or alerts."

    def __init__(self):
        self.llm = Ollama(model="llama3.2")  # You can change to "mistral" or others
        super().__init__()

    def run(self, sensor_data: dict) -> dict:
        # 1. Use tools to assess raw values
        tool_analysis = access_all_vitals(sensor_data)

        # 2. Use LLM to generate a reasoning or summary
        prompt = f"""
        You are a healthcare assistant AI. Here is the patient's data:

        Heart Rate: {sensor_data['heart_rate']} bpm
        Blood Pressure: {sensor_data['blood_pressure']}
        Glucose Level: {sensor_data['glucose_level']} mg/dL
        Oxygen Saturation: {sensor_data['oxygen_saturation']}%

        Initial tool-based assessment:
        {tool_analysis}

        Provide a short health analysis in 2-3 lines. Mention any concern if present.
        """

        llm_response = self.llm.invoke(prompt)

        return {
            "tool_assessment": tool_analysis,
            "llm_analysis": llm_response
        }
