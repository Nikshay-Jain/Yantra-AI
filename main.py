import os
import subprocess
import webbrowser
import pyttsx3
import numpy as np
import pandas as pd
import speech_recognition as sr

# Create an instance of the Text-to-Speech engine
engine = pyttsx3.init()

# Set the properties of the speech output
engine.setProperty("rate", 225)  # Speech speed (words per minute)
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

# Convert text to speech
def say(text):
    engine.say(text)
    engine.runAndWait()

# Understanding Speech said on the microphone
def hear():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.8     # seconds of pause after which the phrase is considered completed.
        audio = r.listen(source)

        try:
            heard = r.recognize_google(audio, language="en-in")
            print("You said:", heard)
        
        except sr.UnknownValueError:
            heard = "Sorry, I could not understand your speech."
            print(heard)

        except sr.RequestError as e:
            heard = "Speech recognition request error:"
            print(heard, str(e))

        return heard

sites = pd.read_csv('sites.csv')
sites.loc[0,'name'] = "google"
sites.loc[0,'web'] = "https://google.com/"
sites.loc[1,'name'] = "youtube"
sites.loc[1,'web'] = "https://youtube.com/"
sites.loc[2,'name'] = "wikipedia"
sites.loc[2,'web'] = "https://wikipedia.com/"
sites.loc[3,'name'] = "chat gpt"
sites.loc[3,'web'] = "https://chat.openai.com/"
sites.loc[4,'name'] = "moodle"
sites.loc[4,'web'] = "https://coursesnew.iitm.ac.in/login/index.php"
sites.sort_values('name', inplace=True)
sites.reset_index(drop=True , inplace=True)

if __name__ == "__main__":
    print('VS Code')
    text = "Nuhmuhstay! Yantruh A.I. is at your command sir!!!"
    say(text)
    #sites = [["google","https://google.com"],["youtube","https://youtube.com"],["wikipedia","https://wikipedia.com"],["chat gpt","https://chat.openai.com/"]]
    while True:
        print("At your Command Sir...")
        cmd = hear()
        if "open" in cmd.lower():
            for site in sites['name']:
                if f"Open {site}".lower() in cmd.lower():
                    say(f"Opening {site} sir...")
                    webbrowser.open(((sites.loc[sites['name']==site]).to_numpy())[0,1])

            #Work on webistes by webdriver package
            
        if "play" in cmd.lower():
            contents = os.listdir(r"C:\Users\Nikshay Jain\OneDrive - smail.iitm.ac.in\Music")
            songs = [os.path.splitext(item)[0] for item in contents]
            for music in songs:
                if music.lower() in cmd.lower():
                    dir = r'C:\Users\Nikshay Jain\OneDrive - smail.iitm.ac.in\Music'
                    file_path = os.path.join(dir, f"{music}.mp3")
                    webbrowser.open(file_path)
                    break
        
        elif "shutdown yantra" in cmd.lower():
            print("Yantra Shutting down...")
            say("Yantra Shutting down")
            break
        
        else:
            say(cmd)