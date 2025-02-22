import streamlit as st
from src.utils.speech_to_text import capture_voice_input
from src.api.gemini_api import get_response_from_gemini
from src.components.ui_elements import show_header

# App Configuration
st.set_page_config(page_title="Voice-Powered Gemini Assistant", layout="centered")

# UI Layout
show_header()

# Voice Input
if st.button("🎤 Start Voice Input"):
    with st.spinner("Listening..."):
        voice_text = capture_voice_input()
        if voice_text:
            st.write(f"**You said:** {voice_text}")
            # Processing using Gemini API
            with st.spinner("Processing..."):
                ai_response = get_response_from_gemini(voice_text)
                st.success("Gemini Response:")
                st.write(ai_response)
        else:
            st.error("Could not understand the voice input. Please try again.")
