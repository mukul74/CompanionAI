import streamlit as st
import requests
import sseclient
import json
import tempfile

st.set_page_config(layout="wide")
st.title("📊 Empowering Elderly Care with Multi-Agent AI System (CompanionAI)")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    if st.button("Upload and Analyze"):
        with st.spinner("Uploading and analyzing..."):

            # Save file temporarily to send as a real file object
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                files = {"file": (uploaded_file.name, f, "text/csv")}
                try:
                    response = requests.post("http://localhost:9000/upload", files=files, stream=True)
                    client = sseclient.SSEClient(response)

                    st.success(f"✅ File `{uploaded_file.name}` upload initiated successfully!")
                    st.subheader("🧾 Patient Analysis Results:")

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown("### 🧍 Patient List")

                    for event in client.events():
                        if event.data.strip():
                            patient_data = json.loads(event.data)
                            idx = patient_data.get("patient_index", "N/A")
                            patient_id = patient_data.get("device_id", f"ID-{idx}")
                            is_critical = patient_data.get("message") == "ALERT TRIGGERED"

                            patient_name = f"Patient #{idx}"
                            color = "red" if is_critical else "green"
                            label = f"<span style='color:{color}'>🔹 {patient_name} ({patient_id})</span>"

                            with col1:
                                with st.expander(label=label, expanded=False):
                                    col2.markdown(f"### 🧍 Details for {patient_name} ({patient_id})")

                                    if is_critical:
                                        col2.error("🚨 **Alert Triggered!**")
                                        col2.markdown(f"- **Reason**: {patient_data['reason']}")
                                        col2.markdown(f"- **Notified**: {patient_data['notify']}")
                                    elif patient_data["message"] == "Unknown output state":
                                        col2.warning("⚠️ Unknown output state.")
                                    else:
                                        col2.info(f"ℹ️ {patient_data['message']}")

                                    if patient_data["analysis"]:
                                        col2.markdown("#### 🧠 LLM Analysis")
                                        col2.write(patient_data["analysis"])
                                    col2.markdown("---", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"⚠️ Could not connect to the API or process stream: {e}")
