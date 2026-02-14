import streamlit as st

st.set_page_config(page_title="Free AI Dental Receptionist", page_icon="🦷")
st.title("🦷 Free AI Dental Receptionist (Browser Voice)")

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

if st.session_state.q_index < len(questions):
    q = questions[st.session_state.q_index]
    st.markdown(f"**AI:** {q}")

    # Browser TTS + Speech Recognition
    st.components.v1.html(f"""
    <button onclick="startConversation()">🎤 Start / Speak</button>
    <p id="result"></p>
    <script>
    let question = `{q}`;
    function speak(text){{
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = 'en-US';
        speechSynthesis.speak(utter);
    }}
    function startConversation(){{
        // Speak the question
        speak(question);
        // Start recognition
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();
        recognition.onresult = function(event){{
            const transcript = event.results[0][0].transcript;
            document.getElementById('result').innerText = 'You said: ' + transcript;
            // Send transcript back to Streamlit via custom event
            const streamlitEvent = new CustomEvent("voice_response", {{detail: transcript}});
            window.dispatchEvent(streamlitEvent);
        }};
    }}
    </script>
    """, height=200)
else:
    st.success("✅ Conversation finished!")
    st.write("Responses collected:")
    st.write(st.session_state.responses)
