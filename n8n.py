import streamlit as st
from gtts import gTTS
import base64
from io import BytesIO

st.set_page_config(page_title="Free AI Dental Receptionist", page_icon="🦷")
st.title("🦷 Free AI Dental Receptionist (Voice)")

# Questions
questions = [
    "Hello! May I have your name, please?",
    "What service do you need?",
    "What date and time would you like your appointment?",
    "Is this urgent or regular?"
]

# Initialize session state
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# Function to generate TTS audio as base64
def tts_audio_base64(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return base64.b64encode(fp.read()).decode()

# ---------------- Conversation Flow ----------------
if st.session_state.q_index < len(questions):
    q = questions[st.session_state.q_index]
    st.markdown(f"**AI:** {q}")

    # Play AI voice
    audio_b64 = tts_audio_base64(q)
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    """
    st.components.v1.html(audio_html, height=50)

    # User voice input (using browser Speech Recognition via HTML + JS)
    st.markdown("Click the button and speak your response:")
    st.components.v1.html(f"""
    <button onclick="startRecognition()">🎤 Speak</button>
    <p id="result"></p>
    <script>
    function startRecognition(){{
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();
        recognition.onresult = function(event){{
            const text = event.results[0][0].transcript;
            document.getElementById('result').innerText = 'You said: ' + text;
            // Send text to Streamlit via Streamlit's custom event
            const streamlitEvent = new CustomEvent("voice_response", {{detail: text}});
            window.dispatchEvent(streamlitEvent);
        }};
    }}
    </script>
    """, height=100)

else:
    st.success("✅ Conversation finished!")
    st.write("Responses collected:")
    st.write(st.session_state.responses)
