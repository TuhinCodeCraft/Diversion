import speech_recognition as sr
import pyautogui
import os
import time

# Function to capture voice input
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand.")
        return None
    except sr.RequestError:
        print("Network error.")
        return None
    execute_command(command)

# Function to execute voice commands
def execute_command(command):
    if "open browser" in command:
        os.system("start chrome")
        time.sleep(2)

    elif "close window" in command:
        pyautogui.hotkey('alt', 'f4')

    elif "scroll down" in command:
        pyautogui.scroll(-300)

    elif "scroll up" in command:
        pyautogui.scroll(300)

    elif "type" in command:
        text_to_type = command.replace("type", "").strip()
        pyautogui.write(text_to_type)

    elif "press enter" in command:
        pyautogui.press('enter')

    elif "shutdown" in command:
        os.system("shutdown /s /t 1")

    elif "open notepad" in command:
        os.system("notepad")

    elif "volume up" in command:
        for _ in range(5):
            pyautogui.press('volumeup')

    elif "volume down" in command:
        for _ in range(5):
            pyautogui.press('volumedown')

    elif "mute" in command:
        pyautogui.press('volumemute')

    else:
        print("Command not recognized.")

listen_command()
