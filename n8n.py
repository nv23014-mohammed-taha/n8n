import streamlit as st
import requests
from io import BytesIO
import base64

# ---------------- CONFIG ----------------
ELEVENLABS_API_KEY = "889605076af6a80e3fa46e8311765b253ef18b6c060c4c94057ba1ed4ff3278a"
ELEVENLABS_VOICE_ID = "pCKbQ4EPGE06zpEPGNvS"

# Questions for the AI receptionist
questions = [
    "Hello! May I have your name, please?",
    "What service do you need?",
    "What date and time would you like your appointment?",
    "Is this urgent or regular?"
]

st.set_page_config(page_title="AI Dental Receptionist", page_icon="🦷", layout="centered")
st.title("🦷 AI Dental Receptionist (Voice)")

# ---------------- FUNCTIONS ----------------
def generate_speech(text):
    """Generate TTS audio from ElevenLabs and return as base64"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        audio_bytes = response.content
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return audio_base64
    else:
        st.error(f"TTS Error: {response.status_code}")
        return None

# ---------------- HTML + JS ----------------
convai_html = f"""
<div id="conversation" style="height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;"></div>
<button onclick="startConversation()">🎤 Start Conversation</button>

<script>
let questions = {questions};
let responses = {{}};
let i = 0;

// Function to play TTS using Streamlit-generated base64 audio
async function speak(text) {{
    const resp = await fetch(`/tts?text=${{encodeURIComponent(text)}}`);
    const data = await resp.text();
    const audio = new Audio('data:audio/mp3;base64,' + data);
    audio.play();
    return new Promise(resolve => audio.onended = resolve);
}}

function startConversation() {{
    nextQuestion();
}}

async function nextQuestion() {{
    if (i < questions.length) {{
        let q = questions[i];
        document.getElementById('conversation').innerHTML += `<b>AI:</b> ${{q}}<br>`;
        
        // Play speech
        await speak(q);

        // Capture user voice
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();
        recognition.onresult = function(event) {{
            const userSpeech = event.results[0][0].transcript;
            responses[q] = userSpeech;
            document.getElementById('conversation').innerHTML += `<b>You:</b> ${{userSpeech}}<br><br>`;
            i++;
            nextQuestion();
        }};
    }} else {{
        alert("✅ Appointment completed! Responses: " + JSON.stringify(responses));
    }}
}}
</script>
"""

# ---------------- STREAMLIT HTML COMPONENT ----------------
st.components.v1.html(convai_html, height=500)

# ---------------- STREAMLIT TTS ENDPOINT ----------------
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from streamlit.runtime.scriptrunner import add_script_run_ctx

app = FastAPI()

@app.get("/tts")
def tts(text: str):
    audio_base64 = generate_speech(text)
    return PlainTextResponse(audio_base64)
