import wave
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from google import genai
from google.genai import types

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

def play_wave(filename):
    """Play WAV file using sounddevice"""
    with wave.open(filename, 'rb') as wf:
        data = wf.readframes(wf.getnframes())
        audio = np.frombuffer(data, dtype=np.int16)
        sd.play(audio, samplerate=wf.getframerate())
        sd.wait()

def listen_to_user():
    """Capture user speech from microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand. Try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

# ------------------- MAIN LOOP -------------------
print("🦷 AI Dental Receptionist started. Say 'exit' to quit.")

while True:
    user_text = listen_to_user()
    if not user_text:
        continue
    if user_text.lower() == "exit":
        print("Exiting AI Dental Receptionist. Goodbye!")
        break

    # Generate Gemini TTS audio
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=user_text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore"  # Ice-style voice
                    )
                )
            ),
        )
    )

    # Extract PCM data
    pcm_data = response.candidates[0].content.parts[0].inline_data.data

    # Save and play audio
    file_name = "gemini_response.wav"
    save_wave(file_name, pcm_data)
    play_wave(file_name)
