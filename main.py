from datetime import datetime
from graphs.health_monitoring_flow import graph

# Simulated sensor data for 5 different patients
test_patients = [
    {
        "timestamp": datetime.now().isoformat(),
        "device_id": "elderly_device_001",
        "heart_rate": 52,
        "blood_pressure": "150/95",
        "glucose_level": 190.0,
        "oxygen_saturation": 89.0,  # 🔴 ALERT PATH
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
        "oxygen_saturation": 98.0,  # ✅ REMINDER PATH
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
        "oxygen_saturation": 88.0,  # 🔴 ALERT PATH
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
        "oxygen_saturation": 97.0,  # ✅ REMINDER PATH
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
        "oxygen_saturation": 85.0,  # 🔴 ALERT PATH
        "movement_activity": "lying",
        "fall_detected": True,
        "impact_force_level": 7.8,
        "post_fall_inactivity_duration": 120,
        "location": "staircase"
    }
]

# Run the graph for each patient and print result
for idx, sensor_data in enumerate(test_patients, 1):
    print("========================================")
    print(f"\n🧑 Patient #{idx} ({sensor_data['device_id']})")
    output = graph.invoke({"input": sensor_data})

    # print("→ Tool Assessment:\n", output["health_report"]["tool_assessment"])
    print("→ LLM Analysis:\n", output["health_report"]["llm_analysis"])

    if output["alert_result"]["raise_alert"]:
        print("🚨 ALERT TRIGGERED:")
        print(output["alert_result"]["reason"])
        print(output["alert_result"]["notify"])
    elif "reminder" in output:
        print("📅 DAILY REMINDER SENT:")
        print(output["reminder"])
    else:
        print("⚠️ Unknown output state:", output)
    print("========================================")
    print("\n")