import pytesseract
from PIL import Image
import pyautogui

# Explicitly set the path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Capture the screen
screenshot = pyautogui.screenshot()

# Save the screenshot (optional)
screenshot.save("screenshot.png")

# Extract text from the screenshot
extracted_text = pytesseract.image_to_string(screenshot)

# Display the extracted text
print("Extracted Text:\n", extracted_text)
