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
engine.setProperty("rate", 225)  # Speech speed (words per minute)
engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

def say(text):
    engine.say(text)
    engine.runAndWait()

# Understanding Speech said on the microphone
def hear():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1     # seconds of pause after which the phrase is considered completed.
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
# sites.loc[0,'name'] = "google"
# sites.loc[0,'web'] = "https://google.com/"
# sites.loc[1,'name'] = "youtube"
# sites.loc[1,'web'] = "https://youtube.com/"
# sites.loc[2,'name'] = "wikipedia"
# sites.loc[2,'web'] = "https://wikipedia.com/"
# sites.loc[3,'name'] = "chat gpt"
# sites.loc[3,'web'] = "https://chat.openai.com/"
# sites.loc[4,'name'] = "moodle"
# sites.loc[4,'web'] = "https://coursesnew.iitm.ac.in/login/index.php"
# sites.loc[5,'name'] = "word"
# sites.loc[5,'web'] = r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
# sites.loc[6,'name'] = "excel"
# sites.loc[6,'web'] = r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
# sites.loc[7,'name'] = "powerpoint"
# sites.loc[7,'web'] = r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"
# sites.loc[8,'name'] = "onenote"
# sites.loc[8,'web'] = r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE"
# sites.loc[9,'name'] = "brave"
# sites.loc[9,'web'] = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
# sites.loc[10,'name'] = "chrome"
# sites.loc[10,'web'] = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# sites.loc[11,'name'] = "edge"
# sites.loc[11,'web'] = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
# sites.loc[12,'name'] = "firefox"
# sites.loc[12,'web'] = r"C:\Program Files\Mozilla Firefox\firefox.exe"
# sites.loc[13,'name'] = "onedrive"
# sites.loc[13,'web'] = r"C:\Program Files\Microsoft OneDrive\OneDrive.exe"

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
    
    if "shutdown" in cmd.lower():
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

        #Work on webistes by webdriver package
        
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
        print("Please tell me the name of the city you want to know the weather of:\n")
        say("Please tell me the name of the city you want to know the weather of:")
        inp = hear()
        rep = api_func.weather(inp)
        say(rep)
        
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
        say("You said" + cmd)