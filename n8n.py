import streamlit as st
import pyttsx3

st.set_page_config(page_title="Free AI Dental Receptionist", page_icon="🦷")
st.title("🦷 Free AI Dental Receptionist (Offline Voice)")

questions = [
    "Hello! May I have your name, please?",
    "What service do you need?",
    "What date and time would you like your appointment?",
    "Is this urgent or regular?"
]

if "responses" not in st.session_state:
    st.session_state.responses = {}
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

if st.session_state.q_index < len(questions):
    q = questions[st.session_state.q_index]
    st.markdown(f"**AI:** {q}")
    
    # Play TTS
    engine.say(q)
    engine.runAndWait()

    # User types response
    user_input = st.text_input("Your Response:")

    if user_input:
        st.session_state.responses[q] = user_input
        st.session_state.q_index += 1
        st.experimental_rerun()
else:
    st.success("✅ Conversation finished!")
    st.write("Responses collected:")
    st.write(st.session_state.responses)
