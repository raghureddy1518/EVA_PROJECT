import speech_recognition as sr
import pyttsx3
import logging
import os
import datetime
import webbrowser
import wikipedia

# This is Logger for the application
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format = "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)

#Taking the male voice from my system

engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

def speak(text):
    """This function converts text to speech.

    Args:
        text 
    return:
        voicce    
    """
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    """This function takes command & recognize

    Returns:
            text as query
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"user said: {query}\n")
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "None"
    return query

#this function will wish you

def wish_me():
    hour = (datetime.datetime.now().hour)
    print(hour)

    if hour >= 0 and hour <= 12:
        speak("Good morning sir! How are you doing?")
    elif hour > 12 and hour < 18:
        speak("Good afternoon sir! Hope you are well.")
    else:
        speak("Good evening sir! How has your day been?")

    speak("I am Eva. Tell me sir, how can I help you?")  


wish_me()
while True:
    
    query = takeCommand().lower()
    print(query)


    if "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"The current time is {strTime}")

    elif "name" in query:
        speak("My name is Eva")

    elif "open google" in query:
        speak("ok sir. please type here what do you want to read")
        webbrowser.open("google.com")

    elif "open youtube" in query:
        speak("ok sir. please type here what do you want to read")
        webbrowser.open("youtube.com")

    elif "open w3schools" in query:
        speak("ok sir. please type here what do you want to read")
        webbrowser.open("w3schools.com")    

    #This query for search something from wikipedia
    elif 'wikipedia' in query:
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
        
    elif "exit" in query:
        speak("Goodbye, sir!")
        exit()