import os
import pyttsx3
import speech_recognition as sr

text = "Hello, I am yuhntra"

# Create an instance of the Text-to-Speech engine
engine = pyttsx3.init()

# Set the properties of the speech output
engine.setProperty("rate", 120)  # Speech speed (words per minute)
engine.setProperty("volume", 1)  # Speech volume (0.0 to 1.0)

# Convert text to speech
engine.say(text)
engine.runAndWait()
