def access_heart_rate(hr: int) -> str:
    if hr < 60:
        return "Heart rate is low (bradycardia)."
    elif hr > 100:
        return "Heart rate is high (tachycardia)."
    else:
        return "Heart rate is normal."

def access_bp(bp: str) -> str:
    try:
        systolic, diastolic = map(int, bp.split("/"))
        if systolic > 140 or diastolic > 90:
            return "High blood pressure (hypertension)."
        elif systolic < 90 or diastolic < 60:
            return "Low blood pressure (hypotension)."
        else:
            return "Blood pressure is normal."
    except:
        return "Invalid blood pressure format."

def access_glucose(glucose: float) -> str:
    if glucose < 70:
        return "Glucose is low (hypoglycemia)."
    elif glucose > 180:
        return "Glucose is high (hyperglycemia)."
    else:
        return "Glucose is in normal range."

def access_spo2(spo2: float) -> str:
    if spo2 < 90:
        return "Low oxygen saturation (possible hypoxia)."
    else:
        return "Oxygen saturation is normal."

def access_movement(activity: str) -> str:
    return f"Movement activity detected: {activity.capitalize()}."

def access_fall(fall: bool) -> str:
    return "Fall detected!" if fall else "No fall detected."

def access_impact(force: float) -> str:
    if force > 5.0:
        return f"High impact force: {force}g (potential injury)."
    elif force > 2.0:
        return f"Moderate impact force: {force}g."
    else:
        return f"Low impact force: {force}g."

def access_inactivity(duration: int) -> str:
    if duration > 60:
        return f"Post-fall inactivity is prolonged ({duration} seconds)."
    else:
        return f"Post-fall inactivity duration: {duration} seconds."

def access_location(loc: str) -> str:
    return f"Current location: {loc.capitalize()}."

def access_all_vitals(data: dict) -> str:
    return "\n".join([
        access_heart_rate(data["heart_rate"]),
        access_bp(data["blood_pressure"]),
        access_glucose(data["glucose_level"]),
        access_spo2(data["oxygen_saturation"]),
        access_movement(data["movement_activity"]),
        access_fall(data["fall_detected"]),
        access_impact(data["impact_force_level"]),
        access_inactivity(data["post_fall_inactivity_duration"]),
        access_location(data["location"]),
    ])
