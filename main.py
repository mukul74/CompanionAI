# from agents.sensor_agent import SensorAgent
# from agents.health_monitor_agent import HealthMonitoringAgent
# from IPython.display import Image
from graphviz import Digraph
from datetime import datetime
from graphs.health_monitoring_flow import graph
# Image(graph.get_graph().draw_mermaid_png())
sensor_data = {
    "timestamp": datetime.now().isoformat(),
    "device_id": "elderly_device_001",
    "heart_rate": 52,
    "blood_pressure": "150/95",
    "glucose_level": 190.0,
    "oxygen_saturation": 89.0
}

output = graph.invoke({"input": sensor_data})
print("\nTool Assessment:\n", output["health_report"]["tool_assessment"])
print("\nLLM Analysis:\n", output["health_report"]["llm_analysis"])
print("Final Output:", output['alert'])
# validated = SensorAgent().run(sensor_data)
# report = HealthMonitoringAgent().run(validated)

# print("\nTool Assessment:\n", report["tool_assessment"])
# print("\nLLM Analysis:\n", report["llm_analysis"])
