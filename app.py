import streamlit as st
from src.utils.speech_to_text import capture_voice_input
from src.api.gemini_api import get_response_from_gemini
from src.components.ui_elements import show_header
from PIL import Image
import pytesseract
import pyautogui


st.set_page_config(page_title="Voice-Powered AI Desktop Assistant", layout="centered")

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
                st.write(ai_response["candidates"][0]["content"]["parts"][0]["text"])
        else:
            st.error("Could not understand the voice input. Please try again.")

# Explicitly set the path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Streamlit UI
st.title("🖼️ Image to Text Extraction with AI Processing")

if st.button("Capture Image"):
    # Display uploaded image
    image = pyautogui.screenshot()

    # Button to start image text extraction
    # if st.button("📄 Extract Text from Image"):
    with st.spinner("Extracting text..."):
        extracted_text = extract_text_from_image(image)
        if extracted_text.strip():
            st.success("Text Extracted Successfully:")
            st.write(f"**Extracted Text:**\n{extracted_text}")
    
        else:
            st.error("No text found in the image. Please try again with a clearer image.")
