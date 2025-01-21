import pyttsx3

text = "Nuhmuhstay! This module is meant to be your text to speech converter. Enter any text to be spoken here and let me try to pronounce it well enough."

# Create an instance of the Text-to-Speech engine
engine = pyttsx3.init()

voices = engine.getProperty('voices')
for v in voices:
    print(v)

# Set the properties of the speech output
engine.setProperty("rate", 175)  # Speech speed (words per minute)
engine.setProperty("volume", 1)  # Speech volume (0.0 to 1.0)
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

# Convert text to speech
engine.say(text)
engine.runAndWait()