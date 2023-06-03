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

# Create an instance of the Text-to-Speech engine
engine = pyttsx3.init()

# Set the properties of the speech output
engine.setProperty("rate", 225)    # Speech speed (words per minute)
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

def say(text):
    engine.say(text)
    engine.runAndWait()

#initialise the microphone
r = sr.Recognizer()
sr.Microphone(device_index=1)

# Adjust the energy threshold dynamically based on the ambient noise level
with sr.Microphone() as source:
    print("Calibrating microphone... Please wait.")
    r.adjust_for_ambient_noise(source)
    print("Calibration complete.")

# Set the desired energy threshold level
energy_threshold = r.energy_threshold * 1.5  # Increase the threshold by a factor (e.g., 1.5)

# Set the energy threshold for speech recognition
r.energy_threshold = energy_threshold

# Understanding Speech said on the microphone
def hear():
    with sr.Microphone() as source:
        #r.pause_threshold = 1     # seconds of pause after which the phrase is considered completed.
        r.listen(source, timeout=4)  # Listen for speech input for a maximum of 5 seconds
        audio = r.listen(source)

        try:
            heard = r.recognize_google(audio)
            print("You said:", heard)
        
        except sr.UnknownValueError:
            heard = "Sorry, I could not understand your speech."
            print(heard)

        except sr.RequestError as e:
            heard = "Speech recognition request error:"
            print(heard, str(e))
            
        return heard

sites = pd.read_csv('sites.csv')
sites.sort_values('name', inplace=True)
sites.reset_index(drop=True , inplace=True)
sites.to_csv("sites.csv",index=False)

text = "Nuhmuhstay! Yantruh A.I. is at your command sir!!!"
print("Namaste! Yantra A.I. is at your command sir!!!")
say(text)
while True:
    f=0
    print("At your Command Sir...")
    cmd = hear()
    
    if "shutdown" in cmd.lower() :
        print("Yantra Shutting down...")
        say("Yantra Shutting down")
        break
        
    elif "open" in cmd.lower():
        for site in sites['name']:
            if f"Open {site}".lower() in cmd.lower():
                say(f"Opening {site} sir...")
                url = sites.loc[sites['name']==site].to_numpy()[0,1]
                if url[0] == 'C':
                    subprocess.Popen(url)
                else:
                    webbrowser.open(url)
                f=1
        if f==0:
            say("Sorry, the app or site you mentioned is not in my database, please enter its name and its url below:")
            name = input("Enter name of site below\n")
            if name == 'q':
                continue
            web = input("Enter its url below\n")
            sites.loc[sites.last_valid_index(),'name'] = name
            sites.loc[sites.last_valid_index(),'web'] = web
        f=0
        
    elif "play" in cmd.lower():
        contents = os.listdir(r"C:\Users\Nikshay Jain\OneDrive - smail.iitm.ac.in\Music")
        songs = [os.path.splitext(item)[0] for item in contents]
        for music in songs:
            if music.lower() in cmd.lower():
                dir = r'C:\Users\Nikshay Jain\OneDrive - smail.iitm.ac.in\Music'
                file_path = os.path.join(dir, f"{music}.mp3")
                webbrowser.open(file_path)
                break

    elif "weather" in cmd.lower():
        print("Please tell me the name of the city you want to know the weather of:")
        say("Please tell me the name of the city you want to know the weather of:")
        inp = hear()
        say(api_func.weather(inp))
        
    elif "news" in cmd.lower():
        print("Please tell me specifically the topic you want the news about:")
        say("Please tell me specifically the topic you want the news about:")
        inp = hear()
        say(api_func.news(inp))

    elif "the time" in cmd.lower():
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"The time currently is {time}")
        say(f"Sir, the time currently is {time}")

    elif "today's date" in cmd.lower() or "date today" in cmd.lower():
        date = datetime.date.today().strftime("%d/%m/%Y")
        print(f"The date today is {date}")
        date_say = datetime.date.today().strftime("%B %d, %Y")
        say(f"The date today is {date_say}")

    else:
        say(cmd)