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

def access_all_vitals(data: dict) -> str:
    return "\n".join([
        access_heart_rate(data["heart_rate"]),
        access_bp(data["blood_pressure"]),
        access_glucose(data["glucose_level"]),
        access_spo2(data["oxygen_saturation"]),
    ])
