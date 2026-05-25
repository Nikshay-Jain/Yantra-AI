import os
import requests
import pyttsx3

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

engine = pyttsx3.init()

# Set the properties of the speech output
engine.setProperty("rate", 200)  # Speech speed (words per minute)
engine.setProperty("voice", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY not found. Add it to your .env file or environment variables.")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found. Add it to your .env file or environment variables.")

def say(text):
    engine.say(text)
    engine.runAndWait()

def weather_report(inp):
    report = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={inp}&aqi=yes"
    )
    return report

def news_report(inp):
    report = requests.get(
        f"https://newsapi.org/v2/everything?q={inp}&from=2023-05-02&sortBy=popularity&apiKey={NEWS_API_KEY}"
    )
    return report