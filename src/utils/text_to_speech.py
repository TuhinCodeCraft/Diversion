import pyttsx3

engine = pyttsx3.init()

text = "Hello, I am your desktop assistant."

engine.setProperty('rate', 200)
engine.setProperty('volume', 1)  

engine.say(text)
engine.runAndWait()