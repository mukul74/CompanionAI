import streamlit as st
import pandas as pd
from graphs.health_monitoring_flow import graph  # Your existing logic

# Streamlit page config
st.set_page_config(page_title="🧑‍⚕️ Companion AI", layout="centered")

# App title
st.title("🧑‍⚕️ Elderly Care Health Monitoring Dashboard")

# Layout: Two columns
left_col, right_col = st.columns([1, 3])

with left_col:
    st.markdown("### 📂 Upload CSV")
    st.markdown(
        "<small>Select a CSV file containing patient data.</small>",
        unsafe_allow_html=True
    )
    uploaded_file = st.file_uploader(" ", type=["csv"])  # Empty label for cleaner look

# Process file and display
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    with right_col:
        st.success(f"✅ {len(df)} patient records uploaded.")
        st.header("👥 Patient Status Overview")

        for idx, row in df.iterrows():
            sensor_data = row.to_dict()

            try:
                output = graph.invoke({"input": sensor_data})
            except Exception as e:
                st.error(f"❌ Failed to process Patient #{idx + 1}: {e}")
                continue

            # Determine status
            is_critical = output["alert_result"]["raise_alert"]
            color = "red" if is_critical else "green"
            alert_title = "🚨 Critical" if is_critical else "✅ Stable"

            with st.expander(f"🧑 Patient #{idx + 1} - {sensor_data.get('device_id', 'N/A')} ({alert_title})", expanded=False):
                st.markdown(f"""
                <div style="background-color:{color};padding:10px;border-radius:10px;">
                    <b>📍 Location:</b> {sensor_data.get('location', 'N/A')}<br>
                    <b>🕒 Timestamp:</b> {sensor_data.get('timestamp', 'N/A')}<br>
                    <b>❤️ Heart Rate:</b> {sensor_data.get('heart_rate', 'N/A')}<br>
                    <b>🩸 Blood Pressure:</b> {sensor_data.get('blood_pressure', 'N/A')}<br>
                    <b>🧪 Glucose Level:</b> {sensor_data.get('glucose_level', 'N/A')}<br>
                    <b>🌬 Oxygen Saturation:</b> {sensor_data.get('oxygen_saturation', 'N/A')}<br>
                    <b>🕺 Activity:</b> {sensor_data.get('movement_activity', 'N/A')}<br>
                    <b>📉 Fall Detected:</b> {sensor_data.get('fall_detected', 'N/A')}<br>
                    <b>💥 Impact Force:</b> {sensor_data.get('impact_force_level', 'N/A')}<br>
                    <b>⏳ Inactivity (Post-Fall):</b> {sensor_data.get('post_fall_inactivity_duration', 'N/A')} sec
                </div>
                """, unsafe_allow_html=True)

                st.subheader("🧠 Overall Analysis")
                st.markdown(output["health_report"]["llm_analysis"])

                if is_critical:
                    st.error(f"**🚨 ALERT** — {output['alert_result']['reason']}")
                    st.write(f"**🔔 Notified:** {output['alert_result']['notify']}")
                elif "reminder" in output:
                    st.success(output["reminder"]["message"])
                else:
                    st.warning("⚠️ No specific action triggered.")

else:
    with right_col:
        st.info("Upload a patient CSV file to start monitoring.")
