from google import genai
from google.genai import types
import wave
import simpleaudio as sa  # for playing audio

# ------------------- CONFIG -------------------
API_KEY = "AIzaSyACm6b0YTARMg4-m66-0m-r-J6TvAe77CU"  # your Gemini API key

client = genai.Client(api_key=API_KEY)

# ------------------- FUNCTIONS -------------------
def save_wave(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio to a WAV file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    print(f"Saved audio to {filename}")

def play_wave(filename):
    """Play WAV file"""
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

# ------------------- GENERATE AUDIO -------------------
text_to_speak = "Say cheerfully: Have a wonderful day!"

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=text_to_speak,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Kore"  # you can try "Puck" or other Gemini voices
                )
            )
        ),
    )
)

# Get audio PCM data
pcm_data = response.candidates[0].content.parts[0].inline_data.data

# Save WAV
file_name = "out.wav"
save_wave(file_name, pcm_data)

# Play audio
play_wave(file_name)
