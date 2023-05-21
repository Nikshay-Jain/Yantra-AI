import os
import subprocess
import webbrowser
import pyttsx3
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
    
if __name__ == "__main__":
    print('VS Code')
    text = "Nuhmuhstay! Yantruh A.I. is at your command sir!!!"
    say(text)
    sites = [["google","https://google.com"],["youtube","https://youtube.com"],["wikipedia","https://wikipedia.com"],["chat gpt","https://chat.openai.com/"]]
    while True:
        print("At your Command Sir...")
        cmd = hear()
        if "open" in cmd.lower():
            for site in sites:
                if f"Open {site[0]}".lower() in cmd.lower():
                    say(f"Opening {site[0]} Sir...")
                    webbrowser.open(site[1])

            #Work on webistes by webdriver package
            if f"Open Music".lower() in cmd.lower():
                cwd = os.getcwd()
                file_path = os.path.join(cwd, "Atrangi Yaari.mp3")
                webbrowser.open(file_path)
        else:
            say(cmd)