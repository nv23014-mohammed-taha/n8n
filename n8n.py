import streamlit as st
import requests
import base64

# ---------------- CONFIG ----------------
ELEVENLABS_API_KEY = "889605076af6a80e3fa46e8311765b253ef18b6c060c4c94057ba1ed4ff3278a"
ELEVENLABS_VOICE_ID = "pCKbQ4EPGE06zpEPGNvS"

# Questions
questions = [
    "Hello! May I have your name, please?",
    "What service do you need?",
    "What date and time would you like your appointment?",
    "Is this urgent or regular?"
]

st.set_page_config(page_title="AI Dental Receptionist", page_icon="🦷", layout="centered")
st.title("🦷 AI Dental Receptionist (Voice)")

# ---------------- FUNCTIONS ----------------
def generate_speech_base64(text):
    """Generate TTS audio from ElevenLabs and return base64 string"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode("utf-8")
    else:
        st.error(f"TTS Error: {response.status_code}")
        return ""

# ---------------- HTML + JS ----------------
convai_html = f"""
<div id="conversation" style="height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;"></div>
<button onclick="startConversation()">🎤 Start Conversation</button>

<script>
let questions = {questions};
let responses = {{}};
let i = 0;

// Function to play ElevenLabs TTS audio
async function speak(text) {{
    const base64Audio = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}`, {{
        method: "POST",
        headers: {{
            "xi-api-key": "{ELEVENLABS_API_KEY}",
            "Content-Type": "application/json"
        }},
        body: JSON.stringify({{text: text}})
    }}).then(res => res.arrayBuffer())
      .then(buffer => btoa(String.fromCharCode(...new Uint8Array(buffer))));
    
    const audio = new Audio('data:audio/mpeg;base64,' + base64Audio);
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
        await speak(q);

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

st.components.v1.html(convai_html, height=500)
