from schemas.states import BaseState
from langgraph.graph import StateGraph, END
from agents.sensor_agent import SensorAgent
from agents.health_monitor_agent import HealthMonitoringAgent
from agents.alert_agent import AlertAgent

sensor = SensorAgent()
health_monitor = HealthMonitoringAgent()
alert = AlertAgent()

def collect_sensor(state):
    return {"sensor_data": sensor.run(state.input)}

def monitor_health(state):
    return {"health_report": health_monitor.run(state.sensor_data)}

def check_alert(state):
    return {"alert": alert.run(state.health_report)}

graph_builder = StateGraph(BaseState)
graph_builder.add_node("CollectSensor", collect_sensor)
graph_builder.add_node("HealthMonitor", monitor_health)
graph_builder.add_node("AlertCheck", check_alert)

graph_builder.set_entry_point("CollectSensor")
graph_builder.add_edge("CollectSensor", "HealthMonitor")
graph_builder.add_edge("HealthMonitor", "AlertCheck")
graph_builder.add_edge("AlertCheck", END)

graph = graph_builder.compile()

