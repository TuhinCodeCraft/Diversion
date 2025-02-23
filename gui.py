import sys
import time
import subprocess
from PyQt5.QtWidgets import QApplication, QLabel, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QPushButton
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QPoint, QSize, QThread, pyqtSignal
import pyautogui
import pyttsx3
import difflib
from src.utils.speech_to_text import capture_voice_input
from src.api.gemini_api import get_response_from_gemini
import pytesseract
from PIL import Image

class VoiceCaptureThread(QThread):
    voice_captured = pyqtSignal(str)

    def run(self):
        while True:
            voice_text = capture_voice_input()
            if voice_text:
                self.voice_captured.emit(voice_text)
            time.sleep(1)

class VoiceAssistantGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Voice Assistant")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(300, 500)

        # GIF Animation
        self.label = QLabel(self)
        self.movie = QMovie("ai.gif")
        self.movie.setScaledSize(QSize(200, 185))
        self.label.setMovie(self.movie)
        self.movie.start()

        # Text output
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)

        # Extract text button
        self.extract_button = QPushButton("Extract Text from Image", self)
        self.extract_button.clicked.connect(self.extract_text_from_image)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.output)
        layout.addWidget(self.extract_button)
        self.setLayout(layout)

        self.commands = {
            "open browser": lambda: subprocess.Popen("chrome"),
            "close window": lambda: self.close_application(),
            "scroll down": lambda: pyautogui.scroll(-300),
            "scroll up": lambda: pyautogui.scroll(300),
            "lock screen": lambda: pyautogui.hotkey('win', 'l'),
            "open notepad": lambda: subprocess.Popen("notepad"),
            "volume up": lambda: [pyautogui.press('volumeup') for _ in range(5)],
            "volume down": lambda: [pyautogui.press('volumedown') for _ in range(5)],
            "mute": lambda: pyautogui.press('volumemute'),
            "play pause": lambda: pyautogui.press('playpause'),
            "next track": lambda: pyautogui.press('nexttrack'),
            "previous track": lambda: pyautogui.press('prevtrack'),
            "show desktop": lambda: pyautogui.hotkey('win', 'd'),
            "open file explorer": lambda: pyautogui.hotkey('win', 'e'),
            "open task manager": lambda: pyautogui.hotkey('ctrl', 'shift', 'esc'),
            "take screenshot": lambda: pyautogui.hotkey('win', 'prtsc'),
            "open calculator": lambda: subprocess.Popen("calc"), 
        }


        self.voice_thread = VoiceCaptureThread()
        self.voice_thread.voice_captured.connect(self.process_voice_input)
        self.voice_thread.start()
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    

    def process_voice_input(self, voice_text):
        voice_text = voice_text.lower()
        self.output.append(f"You said: {voice_text}")

        if voice_text.startswith("nova"):
            prompt = voice_text.replace("nova", "").strip()
            response = self.get_gemini_response(prompt)
            self.output.append(f"Gemini Response: {response}")
            self.text_to_speech(response)
            return

        best_match = self.find_best_match(voice_text, self.commands.keys())
        if best_match:
            self.output.append(f"Executing command: {best_match}")
            self.commands[best_match]()
        else:
            self.output.append("Command not recognized.")

    def get_gemini_response(self, prompt):
        ai_response = get_response_from_gemini(prompt)
        return ai_response["candidates"][0]["content"]["parts"][0]["text"]

    def text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 1)
        engine.say(text)
        engine.runAndWait()

    def find_best_match(self, voice_text, commands):
        best_match = difflib.get_close_matches(voice_text, commands, n=1, cutoff=0.5)
        return best_match[0] if best_match else None

    def close_application(self):
        pyautogui.hotkey('alt', 'f4')

    def extract_text_from_image(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        image = pyautogui.screenshot()
        text = pytesseract.image_to_string(image)
        if text.strip():
            self.output.append(f"Extracted Text:\n{text}")
        else:
            self.output.append("No text found in the image.")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceAssistantGUI()
    window.show()
    sys.exit(app.exec_())
