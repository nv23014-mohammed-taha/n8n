import streamlit as st
from google import genai
from google.genai import types
import numpy as np

# --- CONFIG ---
# WARNING: Do not hardcode your key! Use st.secrets instead.
API_KEY = st.secrets["AIzaSyACm6b0YTARMg4-m66-0m-r-J6TvAe77CU"] 
client = genai.Client(api_key=API_KEY)

st.title("🦷 AI Dental Receptionist")
st.write("Ask about appointments or dental care.")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response with TTS
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                        )
                    ),
                )
            )

            # Extract the audio data
            # The SDK returns raw PCM or optimized audio bytes
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            
            st.write("Here is my response:")
            # Use Streamlit's native audio player (works in browsers!)
            st.audio(audio_data, format="audio/wav", autoplay=True)
            
            st.session_state.messages.append({"role": "assistant", "content": "Sent audio response."})
