from pydantic_ai.agent import Agent
from langchain_community.llms import Ollama
import json
from rich.console import Console
from rich.markdown import Markdown
import requests
class AlertAgent(Agent):
    name = "AlertAgent"
    description = "Evaluates health analysis and decides whether to raise an alert and whom to notify."

    def __init__(self):
        try:
            # Ping remote Ollama server to check if it's up
            requests.get("http://10.103.188.245:11434/api/tags", timeout=2)
            # If reachable, use remote model
            self.llm = Ollama(model="mistral", base_url="http://10.103.188.245:11434/")
            print("[Info] Using remote Ollama model: mistral")
        except Exception as e:
            print(f"[Warning] Remote model unavailable. Reason: {e}")
            print("[Fallback] Using local Ollama model: llama3")
            self.llm = Ollama(model="llama3.2")  # Local host assumed

        # super().__init__()

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

        console = Console()

        console.print("[bold orange][Alert Agent][/bold orange] [cyan] Evaluating report from Health Monitoring Agent[/cyan].")
        console.print("[bold orange][Alert Agent][/bold orange] [bold yellow] Generating alert response[/bold yellow].")

        llm_response = self.llm.invoke(prompt)
        console.print("[bold orange][Alert Agent][/bold orange] [green]Alert response generated.[/green]")
        try:
            alert_info = json.loads(llm_response)
        except Exception as e:
            console.print("[bold red][Alert Agent][/bold red] [red]Failed to parse LLM response, returning fallback.[/red]")
            alert_info = {
                "raise_alert": False,
                "reason": "Failed to parse LLM response.",
                "notify": []
            }

        return alert_info
