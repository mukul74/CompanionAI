from schemas.states import BaseState
from langgraph.graph import StateGraph, END
from agents.sensor_agent import SensorAgent
from agents.health_monitor_agent import HealthMonitoringAgent
from agents.alert_agent import AlertAgent
from agents.daily_reminder_agent import DailyReminderAgent

# Initialize all agents
sensor = SensorAgent()
health_monitor = HealthMonitoringAgent()
alert = AlertAgent()
reminder = DailyReminderAgent()

# Node: Collect sensor data
def collect_sensor(state):
    return {"sensor_data": sensor.run(state.input)}

# Node: Health monitoring
def monitor_health(state):
    return {"health_report": health_monitor.run(state.sensor_data)}

# Node: Handle alert logic
def handle_alert(state):
    alert_result = alert.run(state.health_report)
    return {"alert_result": alert_result}

# Node: Send reminder based on alert result
def send_reminder(state):
    alert_info = state.alert_result
    if alert_info.get("raise_alert", False):
        return {"reminder": "ALERT: Critical condition detected. Notifying concerned parties."}
    else:
        return {"reminder": reminder.run(state.health_report)}

# Build the LangGraph
graph_builder = StateGraph(BaseState)

# Add all nodes
graph_builder.add_node("CollectSensor", collect_sensor)
graph_builder.add_node("HealthMonitor", monitor_health)
graph_builder.add_node("AlertCheck", handle_alert)
graph_builder.add_node("SendReminder", send_reminder)

# Set entry point
graph_builder.set_entry_point("CollectSensor")

# Connect edges
graph_builder.add_edge("CollectSensor", "HealthMonitor")
graph_builder.add_edge("HealthMonitor", "AlertCheck")
graph_builder.add_edge("AlertCheck", "SendReminder")
graph_builder.add_edge("SendReminder", END)

# Compile the graph
graph = graph_builder.compile()
