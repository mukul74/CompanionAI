from pydantic_ai.agent import Agent
from langchain_community.llms import Ollama
import json

class AlertAgent(Agent):
    name = "AlertAgent"
    description = "Evaluates health analysis and decides whether to raise an alert and whom to notify."

    def __init__(self):
        self.llm = Ollama(model="llama3.2")
        super().__init__()

    def run(self, health_report: dict) -> dict:
        prompt = f"""
        You are an alerting system for a healthcare assistant AI.

        Based on the health monitoring report below, determine:
        1. Should an alert be raised?
        2. What is the reason?
        3. Whom should we notify? (Choose from: family, nurse, doctor)

        Respond in valid JSON format with fields:
        {{
            "raise_alert": true/false,
            "reason": "Short explanation",
            "notify": ["family", "nurse", "doctor"]
        }}

        Tool-based Assessment:
        {health_report['tool_assessment']}

        LLM-based Health Analysis:
        {health_report['llm_analysis']}
        """

        print("[Alert Agent] Evaluating health report...")
        llm_response = self.llm.invoke(prompt)

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
