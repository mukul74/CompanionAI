from pydantic_ai.agent import Agent
from langchain_community.llms import Ollama
import datetime

class DailyReminderAgent(Agent):
    name = "DailyReminderAgent"
    description = "Sends daily wellness reminders and checks acknowledgment."

    def __init__(self):
        self.llm = Ollama(model="llama3.2")
        super().__init__()
        self.reminders = [
            "Take your morning medication 💊",
            "Drink a glass of water 💧",
            "Do 10 minutes of light stretching 🧘‍♀️",
            "Check your appointment calendar 📅"
        ]
        self.sent_today = False
        self.acknowledged = False

    def generate_reminder_message(self):
        joined = "\n- " + "\n- ".join(self.reminders)
        prompt = f"""
        It's a new day! Create a warm, supportive daily wellness reminder for an elderly person.
        Include the following tasks:
        {joined}

        Make the tone gentle and cheerful.
        """
        return self.llm.invoke(prompt)

    def run(self, state: dict = None) -> dict:
        if not self.sent_today:
            print("[DailyReminderAgent] Sending first reminder of the day.")
            message = self.generate_reminder_message()
            self.sent_today = True
            self.acknowledged = False
            return {
                "reminder_sent": True,
                "message": message,
                "acknowledgment_required": True
            }

        if self.sent_today and not self.acknowledged:
            print("[DailyReminderAgent] No acknowledgment yet. Sending follow-up.")
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
        print("[DailyReminderAgent] Acknowledgment received.")
        self.acknowledged = True
