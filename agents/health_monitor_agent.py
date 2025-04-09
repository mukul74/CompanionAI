from pydantic_ai.agent import Agent
from langchain_community.llms import Ollama
from tools.access_tools import access_all_vitals
from schemas.sensor_data import SensorData

class HealthMonitoringAgent(Agent):
    name = "HealthMonitoringAgent"
    description = "Analyzes sensor data and provides health insights or alerts."

    def __init__(self):
        self.llm = Ollama(model="llama3.2")  # Change model name if needed
        super().__init__()

    def run(self, sensor_data: dict) -> dict:
        # ✅ Validate data using SensorData schema (ensures all fields exist)
        data = SensorData(**sensor_data)

        # # 1. Use tools to assess core vitals
        # tool_analysis = access_all_vitals(data.dict())

        # # 2. Assess fall risk and movement
        # fall_analysis = self.analyze_fall_and_movement(data)

        # 3. Generate LLM summary

        
        # Tool-based vitals assessment:
        # {tool_analysis}

        # Fall and activity assessment:
        # {fall_analysis}

        prompt = f"""
        You are a proficient healthcare assistant. 
        Process all the sensor data and provide a health report.
        The data includes heart rate, blood pressure, glucose level, oxygen saturation, movement activity, fall detection status, impact force level, post-fall inactivity duration, and location.
        Give a detailed analysis of the patient's health status based on the data provided.
        If any vitals are out of range, provide a warning.
        If a fall is detected, mention the impact force level and inactivity duration.
        If the location is a high-risk area (like bathroom or stairs), mention that as well.
        If the patient is inactive for a long time, mention that too.
        If the patient is active, mention the activity type.
        Give weightage to all the vital signs as per the importance of the data.
        Here is the patient's data:

        Heart Rate: {data.heart_rate} bpm
        Blood Pressure: {data.blood_pressure}
        Glucose Level: {data.glucose_level} mg/dL
        Oxygen Saturation: {data.oxygen_saturation}%
        Movement Activity: {data.movement_activity}
        Fall Detected: {data.fall_detected}
        Impact Force Level: {data.impact_force_level}
        Post-Fall Inactivity Duration: {data.post_fall_inactivity_duration} seconds
        Location: {data.location}
        """
        print("[Health Monitor Agent] Analysing the sensor data including fall and activity.")
        llm_response = self.llm.invoke(prompt)

        return {
            "llm_analysis": llm_response
        }

    def analyze_fall_and_movement(self, data: SensorData) -> str:
        if not data.fall_detected:
            return f"No fall detected. Movement Activity: {data.movement_activity}."
        
        message = ["⚠️ Fall detected."]
        if data.impact_force_level > 5.0:
            message.append("High impact force.")
        if data.post_fall_inactivity_duration > 60:
            message.append("Inactivity period after fall is prolonged.")
        if data.location.lower() in {"bathroom", "stairs", "staircase"}:
            message.append("Fall occurred in a high-risk location.")
        return " ".join(message)
