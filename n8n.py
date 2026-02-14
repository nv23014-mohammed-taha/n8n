from google import genai
from google.genai import types
import wave
import sounddevice as sd
import numpy as np

# ------------------- CONFIG -------------------
API_KEY = "AIzaSyACm6b0YTARMg4-m66-0m-r-J6TvAe77CU"
client = genai.Client(api_key=API_KEY)

# ------------------- FUNCTIONS -------------------
def save_wave(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio to WAV file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    print(f"[✅] Saved audio to {filename}")

def play_wave(filename):
    """Play WAV file using sounddevice"""
    with wave.open(filename, 'rb') as wf:
        data = wf.readframes(wf.getnframes())
        audio = np.frombuffer(data, dtype=np.int16)
        sd.play(audio, samplerate=wf.getframerate())
        sd.wait()

# --------------
print("🦷 AI Dental Receptionist started. Say 'exit' to quit.")

conversation = []

while True:
    user_text = input("\nYou: ")  # Python-only input
    if user_text.lower() == "exit":
        break

    conversation.append({"role": "user", "text": user_text})

    # Generate AI response using Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=user_text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore"
                    )
                )
            ),
        )
    )

    # Extract audio PCM
    pcm_data = response.candidates[0].content.parts[0].inline_data.data
    conversation.append({"role": "assistant", "text": "[Audio Response]"})

    # Save and play
    file_name = "gemini_response.wav"
    save_wave(file_name, pcm_data)
    play_wave(file_name)
