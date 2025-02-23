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
import difflib
import pyttsx3

st.set_page_config(page_title="Voice-Powered AI Desktop Assistant", layout="centered")

show_header()

COMMANDS = {
    "open browser": lambda: subprocess.Popen("chrome"),
    "close window": lambda: close_application(),
    "scroll down": lambda: pyautogui.scroll(-300),
    "scroll up": lambda: pyautogui.scroll(300),
    "lock screen": lambda: pyautogui.hotkey('win', 'l'),
    "open notepad": lambda: subprocess.Popen("notepad"),
    "open file explorer": lambda: pyautogui.hotkey('win', 'e'),
    "open task manager": lambda: pyautogui.hotkey('ctrl', 'shift', 'esc'),
    "switch window": lambda: pyautogui.hotkey('alt', 'tab'),
    "minimize window": lambda: pyautogui.hotkey('win', 'down'),
    "maximize window": lambda: pyautogui.hotkey('win', 'up'),
    "take screenshot": lambda: pyautogui.hotkey('win', 'prtsc'),
    "volume up": lambda: [pyautogui.press('volumeup') for _ in range(5)],
    "volume down": lambda: [pyautogui.press('volumedown') for _ in range(5)],
    "mute": lambda: pyautogui.press('volumemute'),
    "play pause": lambda: pyautogui.press('playpause'),
    "next track": lambda: pyautogui.press('nexttrack'),
    "previous track": lambda: pyautogui.press('prevtrack'),
    "press enter": lambda: pyautogui.press('enter'),
    "press tab": lambda: pyautogui.press('tab'),
    "click": lambda: pyautogui.click(),
    "double click": lambda: pyautogui.doubleClick(),
    "right click": lambda: pyautogui.rightClick(),
    "open settings": lambda: pyautogui.hotkey('win', 'i'),
    "open run": lambda: pyautogui.hotkey('win', 'r'),
    "open calculator": lambda: subprocess.Popen("calc"),
    "show desktop": lambda: pyautogui.hotkey('win', 'd'),
    "search": lambda: pyautogui.hotkey('win', 's')
}
def close_application():
    pyautogui.hotkey('alt', 'f4')
    pyautogui.press('tab')
    pyautogui.press('enter')

def execute_command(command):
    if not command:
        return

    for key in COMMANDS:
        if key in command:
            COMMANDS[key]()
            return

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


def find_best_match(voice_text, commands):
    best_match = difflib.get_close_matches(voice_text, commands, n=1, cutoff=0.5)
    return best_match[0] if best_match else None

st.write("🎤 Voice Input is running continuously...")
while True:
    voice_text = capture_voice_input()
    if voice_text:
        voice_text = voice_text.lower()
        st.write(f"**You said:** {voice_text}")

        if voice_text.startswith("nova"):
            prompt = voice_text.replace("nova", "").strip()
            with st.spinner("Processing with Gemini..."):
                ai_response = get_response_from_gemini(prompt)
                gemini_res = ai_response["candidates"][0]["content"]["parts"][0]["text"]
                st.success("Gemini Response:")
                text_to_speech(gemini_res)
                st.write(gemini_res)
                pyautogui.write(gemini_res)
            continue

        if "write" in voice_text:
            text_to_write = voice_text.replace("write", "").strip()
            pyautogui.write(text_to_write)
            continue

        # Find the closest matching command
        best_match = find_best_match(voice_text, COMMANDS.keys())

        if best_match:
            st.success(f"Executing command: {best_match}")
            execute_command(best_match)
        else:
            st.error("Command not recognized.")

    time.sleep(1)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Streamlit UI
st.title("🖼️ Image to Text Extraction with AI Processing")

if st.button("Capture Image"):

    image = pyautogui.screenshot()

    with st.spinner("Extracting text..."):
        extracted_text = extract_text_from_image(image)
        if extracted_text.strip():
            st.success("Text Extracted Successfully:")
            st.write(f"**Extracted Text:**\n{extracted_text}")

        else:
            st.error("No text found in the image. Please try again with a clearer image.")


# Function to initialize and play text-to-speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()
