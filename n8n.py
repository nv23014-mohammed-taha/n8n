import streamlit as st
from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="AI Dental Receptionist", page_icon="🦷")

# ---------------------------
# SESSION STATE (CRM)
# ---------------------------
if "appointments" not in st.session_state:
    st.session_state.appointments = []

# ---------------------------
# RULE-BASED INTENT DETECTION
# ---------------------------
def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["book", "appointment", "see doctor", "visit"]):
        return "book"
    elif any(word in text for word in ["cancel", "drop", "remove"]):
        return "cancel"
    elif any(word in text for word in ["reschedule", "change", "move"]):
        return "reschedule"
    else:
        return "inquiry"

# ---------------------------
# UI
# ---------------------------
st.title("🦷 Free AI Dental Receptionist")
st.markdown("Simulate an incoming patient call")

transcript = st.text_area("Caller says:")

if st.button("Process Call"):
    if not transcript:
        st.warning("Please enter caller message.")
    else:
        intent = detect_intent(transcript)

        if intent == "book":
            appointment = {
                "name": "Unknown",  # Can add a text input for name
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M"),
                "status": "Booked"
            }
            st.session_state.appointments.append(appointment)
            st.success("✅ Appointment Booked")

        elif intent == "cancel":
            if st.session_state.appointments:
                st.session_state.appointments.pop()
                st.warning("❌ Last Appointment Cancelled")
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
