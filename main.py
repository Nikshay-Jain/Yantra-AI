import os
import datetime
import subprocess
import webbrowser
import urllib.parse
import pyttsx3
import pandas as pd
import numpy as np
import api_func
import speech_recognition as sr
import spacy

# Create an instance of the Text-to-Speech engine
engine = pyttsx3.init()

# Set the properties of the speech output
engine.setProperty("rate", 200)    # Speech speed (words per minute)
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

nlp = spacy.load('en_core_web_sm')

def say(text):
    engine.say(text)
    engine.runAndWait()

#initialise the microphone
r = sr.Recognizer()

# Adjust the energy threshold dynamically based on the ambient noise level
with sr.Microphone() as source:
    print("Calibrating microphone... Please wait.")
    r.adjust_for_ambient_noise(source)
    print("Calibration complete.")

# Set the desired energy threshold level
energy_threshold = r.energy_threshold * 1.5  # Increase the threshold by a factor (e.g., 1.5)

# Set the energy threshold for speech recognition
r.energy_threshold = 300

# Understanding Speech said on the microphone
def hear():
    with sr.Microphone() as source:
        #r.pause_threshold = 1     # seconds of pause after which the phrase is considered completed.
        r.listen(source, timeout=4)  # Listen for speech input for a maximum of 4 seconds
        audio = r.listen(source)

        try:
            heard = r.recognize_google(audio)
            print("You said:", heard)
        
        except sr.UnknownValueError:
            heard = "Sorry, I could not understand your speech."
            print(heard)

        except sr.RequestError as e:
            heard = "Sorry, my speech service is down."
            print(heard, str(e))
            
        return heard

sites = pd.read_csv('sites.csv')
sites.sort_values('name', inplace=True)
sites.reset_index(drop=True , inplace=True)
sites.to_csv("sites.csv",index=False)

def shutdown():
    print("Yantra Shutting down...")
    say("Yantra Shutting down")
    exit()

def greet():
    say("Hello! How are you?")

def introduce():
    say("I am Yantra, your desktop assistant.")

def handle_user_name():
    say("I don't know your name yet. Can you please tell me your name?")
    user_name = input()
    if user_name:
        say(f"Nice to meet you, {user_name}!")
        return user_name
    return None

def open_website_or_app(cmd):
    f = 0
    for site in sites['name']:
        if f"open {site}".lower() in cmd:
            say(f"Opening {site}...")
            url = sites.loc[sites['name'] == site, 'web'].values[0]
            if url[0] == 'C':
                subprocess.Popen(url)
            else:
                webbrowser.open(url)
            f = 1
    # if f == 0:
    #     say("Sorry, the app or site you mentioned is not in my database. Please enter its name and URL below:")
    #     name = input("Enter name of site below\n")
    #     if name.lower() == 'q':
    #         return
    #     web = input("Enter its URL below\n")
    #     sites.loc[len(sites)] = [name, web]

def add_site_to_database(name, url):
    """Add a new site to the database."""
    sites.loc[len(sites)] = [name, url]

def play_music(cmd):
    music_dir = r"C:\Users\Nikshay Jain\OneDrive - smail.iitm.ac.in\Music"
    contents = os.listdir(music_dir)
    songs = [os.path.splitext(item)[0] for item in contents]
    for music in songs:
        if music.lower() in cmd:
            file_path = os.path.join(music_dir, f"{music}.mp3")
            webbrowser.open(file_path)
            break

def get_weather():
    say("Please tell me the name of the city you want to know the weather of:")
    city = input()
    if city:
        # Use an appropriate function to get the weather for the city
        weather_info = api_func.weather(city)
        say(weather_info)

def get_news():
    say("Please tell me specifically the topic you want the news about:")
    topic = input()
    if topic:
        # Use an appropriate function to get the news for the topic
        news_info = api_func.news(topic)
        say(news_info)

def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"The time currently is {current_time}")
    say(f"The time currently is {current_time}")

def tell_date():
    current_date = datetime.date.today().strftime("%d/%m/%Y")
    print(f"The date today is {current_date}")
    date_say = datetime.date.today().strftime("%B %d, %Y")
    say(f"The date today is {date_say}")

def parse_command(cmd):
    """Parse the command using spaCy."""
    doc = nlp(cmd)
    return doc

def main():
    text = "Nuhmuhstay! Yantruh is at your command!!!"
    print("Namaste! Yantra is at your command!!!")
    say(text)
    user_name = ""
    while True:
        print("At your Command...")
        cmd = input().lower()

        doc = parse_command(cmd)

        # Shutdown command
        if any(token.lemma_ in ["shutdown", "exit", "quit"] for token in doc):
            shutdown()
        
        # Greeting command
        elif "hello" in cmd:
            greet()
        
        # Introduction command
        elif "your name" in cmd:
            introduce()
        
        # User name command
        elif "my name" in cmd:
            if user_name:
                say(f"Your name is {user_name}.")
            else:
                user_name = handle_user_name()
        
        # Open website or app command
        elif any(token.lemma_ in ["open"] for token in doc):
            for token in doc:
                if token.lemma_ == "open":
                    site_name = token.head.text
                    if site_name in sites['name'].values:
                        open_website_or_app(site_name)
                    else:
                        say("Sorry, the app or site you mentioned is not in my database. Please enter its name and URL below:")
                        name = input("Enter name of site below\n")
                        if name.lower() == 'q':
                            break
                        url = input("Enter its URL below\n")
                        add_site_to_database(name, url)
                    break
        
        # Play music command
        elif any(token.lemma_ in ["play"] for token in doc):
            for token in doc:
                if token.lemma_ == "play":
                    song_name = token.head.text
                    play_music(song_name)
                    break
        
        # Weather command
        elif any(token.lemma_ in ["weather"] for token in doc):
            say("Please tell me the name of the city you want to know the weather of:")
            city = hear()
            if city:
                get_weather(city)
        
        # News command
        elif any(token.lemma_ in ["news"] for token in doc):
            say("Please tell me specifically the topic you want the news about:")
            topic = hear()
            if topic:
                get_news(topic)
        
        # Time command
        elif any(token.lemma_ in ["time"] for token in doc):
            tell_time()
        
        # Date command
        elif any(token.lemma_ in ["date"] for token in doc):
            tell_date()
        
        else:
            say("I am sorry, I cannot do that yet.")

if __name__ == "__main__":
    main()