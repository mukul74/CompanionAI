from datetime import datetime
from graphs.health_monitoring_flow import graph
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Rich console
console = Console()

# Simulated sensor data for 5 different patients
test_patients = [
    {
        "timestamp": datetime.now().isoformat(),
        "device_id": "elderly_device_001",
        "heart_rate": 52,
        "blood_pressure": "150/95",
        "glucose_level": 190.0,
        "oxygen_saturation": 89.0,
        "movement_activity": "lying",
        "fall_detected": True,
        "impact_force_level": 6.2,
        "post_fall_inactivity_duration": 80,
        "location": "bathroom"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "device_id": "elderly_device_002",
        "heart_rate": 72,
        "blood_pressure": "120/80",
        "glucose_level": 110.0,
        "oxygen_saturation": 98.0,
        "movement_activity": "walking",
        "fall_detected": False,
        "impact_force_level": 0.0,
        "post_fall_inactivity_duration": 0,
        "location": "living room"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "device_id": "elderly_device_003",
        "heart_rate": 105,
        "blood_pressure": "145/100",
        "glucose_level": 200.0,
        "oxygen_saturation": 88.0,
        "movement_activity": "sitting",
        "fall_detected": True,
        "impact_force_level": 3.4,
        "post_fall_inactivity_duration": 20,
        "location": "kitchen"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "device_id": "elderly_device_004",
        "heart_rate": 68,
        "blood_pressure": "118/79",
        "glucose_level": 95.0,
        "oxygen_saturation": 97.0,
        "movement_activity": "idle",
        "fall_detected": False,
        "impact_force_level": 0.0,
        "post_fall_inactivity_duration": 0,
        "location": "bedroom"
    },
    {
        "timestamp": datetime.now().isoformat(),
        "device_id": "elderly_device_005",
        "heart_rate": 110,
        "blood_pressure": "160/105",
        "glucose_level": 210.0,
        "oxygen_saturation": 85.0,
        "movement_activity": "lying",
        "fall_detected": True,
        "impact_force_level": 7.8,
        "post_fall_inactivity_duration": 120,
        "location": "staircase"
    }
]

# Run the graph for each patient and pretty-print the results
for idx, sensor_data in enumerate(test_patients, 1):
    console.rule(f"🧑 Patient #{idx} — {sensor_data['device_id']}", style="bold green")
    output = graph.invoke({"input": sensor_data})

    # Tool Assessment (optional)
    # console.print(Panel.fit(output["health_report"]["tool_assessment"], title="🛠️ Tool Assessment", style="dim"))

    # LLM Analysis
    console.print(Panel.fit(output["health_report"]["llm_analysis"], title="🧠 LLM Analysis", style="cyan"))

    # Alert Handling
    if output["alert_result"]["raise_alert"]:
        console.print(Panel.fit(
            f"[bold red]🚨 ALERT TRIGGERED[/bold red]\n\n"
            f"[b]Reason:[/b] {output['alert_result']['reason']}\n"
            f"[b]Notified:[/b] {output['alert_result']['notify']}",
            title="🔴 Critical Health Alert", style="bold red"
        ))
    elif "reminder" in output:
        console.print(Panel.fit(
            output["reminder"]["message"],
            title="📅 Daily Reminder", style="green"
        ))
    else:
        console.print("[yellow]⚠️ Unknown output state[/yellow]")
    
    console.rule("End of Patient Report", style="dim")
    print("\n")
