from pydantic_ai.agent import Agent
from langchain_community.llms import Ollama
import json

class AlertAgent(Agent):
    name = "AlertAgent"
    description = "Evaluates health analysis and decides whether to raise an alert and whom to notify."

    def __init__(self):
        self.llm = Ollama(model="llama3.2")
        super().__init__()
        #    Tool-based Assessment:
        # {health_report['tool_assessment']}
    def run(self, health_report: dict) -> dict:
        prompt = f"""
        You are an alerting system for a healthcare assistant AI.
        Your task is to evaluate the health monitoring report and determine if an alert should be raised.
        Use {health_report['llm_analysis']}, which includes vital signs, fall detection status, and other health indicators.
        You need to analyze the report and decide if the patient's condition is critical enough to warrant an alert.
        If an alert is raised, provide a reason and specify whom to notify (family, nurse, doctor).

        
        Based on the health monitoring report below, determine:
        1. Should an alert be raised?
        2. What is the reason?
        3. Whom should we notify? (Choose from: family, nurse, doctor)

        Respond in valid JSON format with fields:
        {{
            "raise_alert": true/false,
            "reason": "Short explanation",
            "notify": ["Family", "Nurse", "Doctor"]
        }}

        Ensure the response is concise and clear and in points.
        """

        print("[Alert Agent] Evaluating report from Health Monitoring Agent.")
        print("[Alert Agent] Generating alert response.")
        llm_response = self.llm.invoke(prompt)
        print("[Alert Agent] Alert response generated.")
        try:
            alert_info = json.loads(llm_response)
        except Exception as e:
            print("[Alert Agent] Failed to parse LLM response, returning fallback.")
            alert_info = {
                "raise_alert": False,
                "reason": "Failed to parse LLM response.",
                "notify": []
            }

        return alert_info
