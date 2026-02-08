# app.py

import streamlit as st
import requests
from io import BytesIO
import streamlit.components.v1 as components

# ========== CONFIGURATION ==========
ELEVENLABS_API_KEY = "889605076af6a80e3fa46e8311765b253ef18b6c060c4c94057ba1ed4ff3278a"
ELEVENLABS_VOICE_ID = "pCKbQ4EPGE06zpEPGNvS"
N8N_WEBHOOK_URL = "https://mohammednabeel.app.n8n.cloud/webhook-test/c3e6a86b-12cd-44e9-b764-5200e302a562"

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="ElevenLabs TTS + ConvAI + n8n", page_icon="🤖", layout="centered")

st.title("🤖 ElevenLabs Text‑to‑Speech + ConvAI + n8n Integration")
st.write("Enter text below to generate speech, trigger your n8n workflow, or interact with the embedded ConvAI agent.")

# ——— TEXT‑TO‑SPEECH SECTION ———
st.header("🎧 Text‑to‑Speech Generator")

text_input = st.text_area("Enter your text here:", height=150)

if st.button("Generate TTS Audio"):
    if not text_input.strip():
        st.error("⚠️ Please enter some text first.")
    else:
        with st.spinner("Generating audio…"):
            try:
                tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
                headers = {
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json"
                }
                payload = {"text": text_input}

                response = requests.post(tts_url, headers=headers, json=payload)

                if response.status_code == 200:
                    audio_bytes = response.content
                    st.success("✅ Audio generated!")

                    # play audio
                    st.audio(audio_bytes, format="audio/mp3")

                    # download button
                    st.download_button(
                        label="⬇️ Download Audio",
                        data=BytesIO(audio_bytes),
                        file_name="speech.mp3",
                        mime="audio/mp3"
                    )

                    # send text to n8n webhook
                    n8n_resp = requests.post(N8N_WEBHOOK_URL, json={"text": text_input})
                    if n8n_resp.status_code in [200, 201]:
                        st.info("🟢 n8n workflow triggered successfully!")
                    else:
                        st.warning(f"⚠️ n8n webhook failed (status {n8n_resp.status_code}).")
                else:
                    st.error(f"❌ TTS request failed (status {response.status_code}).")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

st.markdown("---")

# ——— ConvAI EMBED SECTION ———
st.header("💬 ElevenLabs ConvAI Chatbot")

convai_html = """
<elevenlabs-convai agent-id="agent_3401kgwwqaecertangz4492v820c"></elevenlabs-convai>
<script src="https://unpkg.com/@elevenlabs/convai-widget-embed" async type="text/javascript"></script>
"""

components.html(convai_html, height=600)

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, ElevenLabs, and n8n")
