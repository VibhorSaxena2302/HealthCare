import streamlit as st
import os
from dotenv import load_dotenv
import json
import google.generativeai as genai
import speech_recognition as sr
from google.cloud import texttospeech_v1
import io
import base64

# Load environment variables
def page():

    test_style = """
    <style>
    [data-testid="stApp"] {
        background-image: -webkit-gradient(linear, left top, left bottom, from(rgba(255,255,255, .7)), to(rgba(0, 0, 0, 0.30))), url("https://i.pinimg.com/474x/54/f2/b3/54f2b3d4bbf33ee2afe399d7ad0d7fad.jpg");
       background-size: cover;  /*Scales the image to cover the entire background */
        background-repeat: no-repeat; /* Prevents the image from repeating */
        background-position: center; /* Centers the image */
        }
    </style>
    """
    st.markdown(test_style, unsafe_allow_html=True)

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\banya\OneDrive\Desktop\health3.0\HealthCare\LLM\google_cloud_api\storage-441514-c40e275bbda9.json" 
    os.environ['GENAI_API_KEY'] = "AIzaSyAuV8NpDDi32rjEd_1FkiqMMYYkqEUevPw"

    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")

    if not api_key:
        st.error("Please set the GENAI_API_KEY environment variable.")
        st.stop()

    # Configure the Generative AI API
    genai.configure(api_key=api_key)

    # Set up model configuration and safety settings
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    # Initialize Google Cloud Text-to-Speech client
    tts_client = texttospeech_v1.TextToSpeechClient()

    # Load conversation history from file into session state for reference but do not display it
    if "conversation_history" not in st.session_state:
        history_file = r"C:\Users\banya\OneDrive\Desktop\health3.0\HealthCare\LLM\empathic_chatbot\conversation_history_granny.json"
        if os.path.exists(history_file):
            with open(history_file, "r") as file:
                st.session_state.conversation_history = json.load(file)
        else:
            st.session_state.conversation_history = []

    # Initialize an empty list to hold only the session's live conversation messages
    if "displayed_conversation" not in st.session_state:
        st.session_state.displayed_conversation = []

    # Start chat with existing conversation history
    convo = model.start_chat(history=st.session_state.conversation_history)

    # Define the GrandmaBot prompt for each message
    prompt = (
        "You are GrandmaBot, a elderly woman with a gentle, understanding tone. never answer in points, answer should be like a reply in real life conversation. Answer should be within 500 characters"
    )

    # Display title and introduction
    st.title("GrandmaBot")
    st.subheader("Welcome, dear! I'm here to listen, share a bit of my wisdom, and offer support. 🌸")

    # Display only the current session's conversation
    for message in st.session_state.displayed_conversation:
        role = message["role"]
        parts = message["parts"][0]
        if role == "user":
            st.chat_message("User").markdown(parts)
        elif role == "model":
            st.chat_message("GrandmaBot").markdown(parts)

    st.write('---')
    
    # User input and response handling
    user_input = st.text_input("Type your message here:", key="user_input")

    # Add speech-to-text functionality when spacebar is pressed
    if st.button("Start Speech Recognition (Press Spacebar to Speak)"):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            st.write("Listening... Please speak!")
            audio = recognizer.listen(source)
        
        try:
            user_input = recognizer.recognize_google(audio)
            st.write(f"You said: {user_input}")
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
    
    if st.button("Send") or user_input:
        if user_input:
            # Append user message to both the full conversation history and the displayed session conversation
            user_message = {"role": "user", "parts": [user_input]}
            st.session_state.conversation_history.append(user_message)
            st.session_state.displayed_conversation.append(user_message)

            with st.spinner("Thinking..."):
                # Get bot's response with prompt appended to user input
                combined_input = f"{prompt}\n\n{user_input}"
                convo.send_message(combined_input)
                bot_response = convo.last.text
                
                # Append bot response to both the full history and displayed conversation
                bot_message = {"role": "model", "parts": [bot_response]}
                st.session_state.conversation_history.append(bot_message)
                st.session_state.displayed_conversation.append(bot_message)
                
                # Display user input and bot response
                st.chat_message("User").markdown(user_input)
                st.chat_message("GrandmaBot").markdown(bot_response)

                ssml_text = f"""
                <speak>
                    <prosody rate="95%" pitch="-4st">{bot_response}</prosody>
                </speak>
                """
                synthesis_input = texttospeech_v1.SynthesisInput(ssml=ssml_text)
                voice = texttospeech_v1.VoiceSelectionParams(
                    language_code="en-IN",
                    name="en-US-Wavenet-C",  # Mature, feminine voice
                    ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
                )
                audio_config = texttospeech_v1.AudioConfig(
                    audio_encoding=texttospeech_v1.AudioEncoding.MP3
                )
                response = tts_client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

                # Stream audio using BytesIO without saving to disk
                audio_stream = io.BytesIO(response.audio_content)
                audio_base64 = base64.b64encode(audio_stream.read()).decode("utf-8")
                audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)

        else:
            st.warning("Please enter a message before sending.")