import streamlit as st
import requests
from io import BytesIO
import streamlit.components.v1 as components

# ---------- CONFIG ----------
ELEVENLABS_API_KEY = "889605076af6a80e3fa46e8311765b253ef18b6c060c4c94057ba1ed4ff3278a"
ELEVENLABS_VOICE_ID = "pCKbQ4EPGE06zpEPGNvS"
N8N_WEBHOOK_URL = "https://mohammednabeel.app.n8n.cloud/webhook-test/c3e6a86b-12cd-44e9-b764-5200e302a562"

# ---------- QUESTIONS ----------
questions = [
    "Hello! May I have your name, please?",
    "What service do you need?",
    "What date and time would you like your appointment?",
    "Is this urgent or regular?"
]

# Store responses
appointment = {}

st.set_page_config(page_title="AI Dental Receptionist", page_icon="🦷", layout="centered")
st.title("🦷 AI Dental Receptionist (Voice)")

# ---------- FUNCTIONS ----------
def generate_speech(text):
    """Generates speech audio from ElevenLabs TTS"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"TTS Error: {response.status_code}")
        return None

# ---------- VOICE CONVERSATION HTML ----------
st.header("Voice Conversation")
st.write("Click start, speak your answers, and the AI will guide you.")

convai_html = f"""
<div id="conversation"></div>
<button onclick="startConversation()">🎤 Start Conversation</button>
<script>
let questions = {questions};
let responses = {{}};
let i = 0;

async function speak(text) {{
    const audioResp = await fetch('data:audio/mp3;base64,' + '{""}');
}}

function startConversation() {{
    nextQuestion();
}}

function nextQuestion() {{
    if (i < questions.length) {{
        let q = questions[i];
        // Display question
        document.getElementById('conversation').innerHTML += `<b>AI:</b> ${q}<br>`;
        
        // Play TTS audio via Streamlit Python
        fetch(`/tts?text=${encodeURIComponent(q)}`)
            .then(response => response.blob())
            .then(blob => {{
                let audioURL = URL.createObjectURL(blob);
                let audio = new Audio(audioURL);
                audio.play();
            }});
        
        // Capture voice after delay
        setTimeout(() => {{
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.start();
            recognition.onresult = function(event) {{
                const userSpeech = event.results[0][0].transcript;
                responses[q] = userSpeech;
                document.getElementById('conversation').innerHTML += `<b>You:</b> ${userSpeech}<br><br>`;
                i++;
                nextQuestion();
            }};
        }}, 4000);
    }} else {{
        // Send responses to Streamlit
        fetch(`/submit?data=${encodeURIComponent(JSON.stringify(responses))}`)
            .then(response => alert("✅ Appointment sent! Check your email."));
    }}
}}
</script>
"""

components.html(convai_html, height=600)
