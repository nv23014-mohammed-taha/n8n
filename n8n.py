import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="AI Dental Receptionist", page_icon="🦷")

# ---------------------------
# Secure API Key from Streamlit Secrets
# ---------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found. Add it in Streamlit Cloud Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------
# Session State (Simple CRM)
# ---------------------------
if "appointments" not in st.session_state:
    st.session_state.appointments = []

# ---------------------------
# Intent Detection via GPT
# ---------------------------
def detect_intent(text):

    prompt = f"""
    Extract structured JSON:
    {{
        "intent": "book | cancel | reschedule | inquiry",
        "name": "",
        "date": "",
        "time": ""
    }}

    Text: {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {"intent": "inquiry"}

# ---------------------------
# UI
# ---------------------------
st.title("🦷 AI Dental Receptionist")
st.markdown("Simulate incoming patient call")

transcript = st.text_area("Caller says:")

if st.button("Process Call"):

    if not transcript:
        st.warning("Please enter caller message.")
        st.stop()

    result = detect_intent(transcript)
    intent = result.get("intent")

    if intent == "book":
        appointment = {
            "name": result.get("name"),
            "date": result.get("date"),
            "time": result.get("time"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.appointments.append(appointment)
        st.success("✅ Appointment Booked")

    elif intent == "cancel":
        if st.session_state.appointments:
            st.session_state.appointments.pop()
            st.warning("❌ Appointment Cancelled")
        else:
            st.info("No appointments found.")

    elif intent == "reschedule":
        st.info("🔁 Rescheduling logic placeholder.")

    else:
        st.info("ℹ️ General inquiry detected.")

# ---------------------------
# CRM Dashboard
# ---------------------------
st.divider()
st.subheader("📋 Appointment Records")

if st.session_state.appointments:
    st.dataframe(st.session_state.appointments)
else:
    st.write("No appointments yet.")
