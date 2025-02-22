import streamlit as st
from src.utils.speech_to_text import capture_voice_input
from src.api.gemini_api import get_response_from_gemini
from src.components.ui_elements import show_header
from PIL import Image
import pytesseract
import pyautogui
import speech_recognition as sr
import os
import time
import subprocess



st.set_page_config(page_title="Voice-Powered AI Desktop Assistant", layout="centered")

show_header()

COMMANDS = {
    "open browser": lambda: subprocess.Popen("chrome"),
    "close window": lambda: pyautogui.hotkey('alt', 'f4'),
    "scroll down": lambda: pyautogui.scroll(-300),
    "scroll up": lambda: pyautogui.scroll(300),
    "shutdown": lambda: os.system("shutdown /s /t 1"),
    "open notepad": lambda: subprocess.Popen("notepad"),
    "volume up": lambda: [pyautogui.press('volumeup') for _ in range(5)],
    "volume down": lambda: [pyautogui.press('volumedown') for _ in range(5)],
    "mute": lambda: pyautogui.press('volumemute'),
    "click": lambda: pyautogui.click(),
    "double click": lambda: pyautogui.doubleClick(),
    "right click": lambda: pyautogui.rightClick()
}

# Function to capture voice input
# def listen_command():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#     try:
#         command = recognizer.recognize_google(audio).lower()
#         print(f"You said: {command}")
#         return command
#     except sr.UnknownValueError:
#         print("Sorry, I did not understand.")
#         return None
#     except sr.RequestError:
#         print("Network error.")
#         return None

# Function to execute voice commands
def execute_command(command):
    if not command:
        return

    # Check if command matches a pre-defined action
    for key in COMMANDS:
        if key in command:
            COMMANDS[key]()
            return

    # Dynamic actions
    if "type" in command:
        text_to_type = command.replace("type", "").strip()
        pyautogui.write(text_to_type)

    elif "press" in command and "and" in command:
        keys = command.replace("press", "").strip().split(" and ")
        keys = [key.strip() for key in keys]
        pyautogui.hotkey(*keys)

    elif "move mouse to" in command:
        try:
            _, x, y = command.split()[-2:]
            pyautogui.moveTo(int(x), int(y))
        except ValueError:
            print("Invalid coordinates")

    elif "drag mouse to" in command:
        try:
            _, x, y = command.split()[-2:]
            pyautogui.dragTo(int(x), int(y), duration=1)
        except ValueError:
            print("Invalid coordinates")

    else:
        print("Command not recognized.")

# Infinite loop to keep listening
# while True:
#     command = listen_command()
#     execute_command(command)
#     time.sleep(1)  # Optional delay to avoid overwhelming the microphone

# Voice Input
if st.button("🎤 Start Voice Input"):
    with st.spinner("Listening..."):
        voice_text = capture_voice_input().lower()
        if voice_text not in COMMANDS:
            st.write(f"**You said:** {voice_text}")
            # Processing using Gemini API
            with st.spinner("Processing..."):
                ai_response = get_response_from_gemini(voice_text)
                st.success("Gemini Response:")
                st.write(ai_response["candidates"][0]["content"]["parts"][0]["text"])
        else:
            execute_command(voice_text)
            
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
