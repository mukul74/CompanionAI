from pydantic_ai.agent import Agent
from langchain_community.llms import Ollama
import datetime
from rich.console import Console
import requests
class DailyReminderAgent(Agent):
    name = "DailyReminderAgent"
    description = "Sends daily wellness reminders and checks acknowledgment."

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
            self.reminders = [
                "Take your morning walk ",
                "Eat a healthy breakfast",
                "Check your blood pressure",
                "Take your vitamins",
                "Read a book or do a puzzle",
                "Call a friend or family member",
                "Do some light housework",
                "Practice deep breathing exercises",
                "Listen to your favorite music",
                "Spend some time in the garden",
                "Watch a favorite TV show or movie",
                "Write in a journal or diary",
                "Take your morning medication",
                "Drink a glass of water",
                "Do 10 minutes of light stretching",
                "Check your appointment calendar"
            ]
            self.sent_today = False
            self.acknowledged = False

    def generate_reminder_message(self, health_report: dict):
        joined = "\n- " + "\n- ".join(self.reminders)
        prompt = f"""
        You are a friendly assistant for an elderly person.
        Your task is to send a daily wellness reminder.
        The date is: {datetime.datetime.now().strftime('%Y-%m-%d')} 
        The time is: {datetime.datetime.now().strftime('%H:%M')}
        The person is elderly and may need a gentle reminder to take care of themselves.
        The reminders should be simple and easy to follow.
        Decide the tasks {joined}, you can modify them, after analysing {health_report['llm_analysis']}:

        Return message in points.
        
        """
        return self.llm.invoke(prompt)

    def run(self, health_report: dict) -> dict:
        if not self.sent_today:
            console = Console()
            console.print("[bold blue][Daily Reminder Agent][/bold blue] [yellow]Generating relevant reminders of the day.[/yellow]")
            message = self.generate_reminder_message(health_report)
            console.print("[bold blue][Daily Reminder Agent][/bold blue] [green]Sending reminders of the day.[/green]")
            # print("[Daily Reminder Agent] Sensding reminders of the day.")
            self.sent_today = True
            self.acknowledged = False
            return {
                "reminder_sent": True,
                "message": message,
                "acknowledgment_required": True
            }

        if self.sent_today and not self.acknowledged:
            print("[Daily Reminder Agent] No acknowledgment yet. Sending follow-up.")
            return {
                "reminder_sent": True,
                "message": "Just checking in 😊 — Have you done your morning wellness tasks?",
                "acknowledgment_required": True
            }

        return {
            "reminder_sent": False,
            "message": "No reminder needed at this time.",
            "acknowledgment_required": False
        }

    def acknowledge(self):
        print("[Daily Reminder Agent] Acknowledgment received.")
        self.acknowledged = True
