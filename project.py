import speech_recognition as sr
import pyttsx3
import logging
import os
import datetime
import webbrowser
import wikipedia
import random
import requests
import subprocess  # For opening applications

# Logging configuration
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)
logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

def speak(text):
    """This function converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    """This function listens to voice input and returns the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            speak("")
        except sr.RequestError as e:
            speak("There seems to be a problem connecting to the service.")
            logging.error(f"Speech recognition service error: {e}")
        return None

def wish_me():
    """This function wishes the user based on the current time."""
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good morning sir! How are you doing?")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon sir! Hope you are well.")
    else:
        speak("Good evening sir! How has your day been?")
    speak("I am Eva. How can I assist you today?")

# Feature: Open website
def open_website(command):
    """This function opens a website based on the command."""
    try:
        if "open" in command:
            website = command.replace("open", "").strip()
            if "." not in website:  # If no dot in the input, assume it's a common site
                website = f"www.{website}.com"
            elif not website.startswith(("http://", "https://")):
                website = f"http://{website}"
            webbrowser.open(website)
            speak(f"Opening {website}")
        else:
            speak("Sorry, I couldn't understand the website name.")
    except Exception as e:
        speak("Sorry, I couldn't open the website.")
        logging.error(f"Failed to open website: {e}")

# Feature: Open application or fallback to website
def open_application_or_website(command):
    """This function opens an application, and if not found, tries to open it as a website."""
    try:
        app_name = command.replace("open", "").strip().lower()
        # List of common applications and their executable names
        app_mapping = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "word": "winword.exe",  # Microsoft Word
            "excel": "excel.exe",  # Microsoft Excel
            "chrome": "chrome.exe",  # Google Chrome
            "paint": "mspaint.exe",
        }

        if app_name in app_mapping:
            app_path = app_mapping[app_name]
            subprocess.Popen(app_path)
            speak(f"Opening {app_name}")
        else:
            speak(f" trying to open {app_name} as a website.")
            open_website(f"open {app_name}")
    except Exception as e:
        speak("Sorry, I couldn't open the application or website.")
        logging.error(f"Failed to open application or website: {e}")

# Feature: Search Wikipedia
def search_wikipedia(query):
    """Searches and speaks a summary from Wikipedia."""
    query = query.replace("wikipedia", "").strip()
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    except Exception as e:
        speak("Sorry, I couldn't fetch information from Wikipedia.")
        logging.error(f"Wikipedia error: {e}")

# Feature: Joke
def tell_joke():
    """Tells a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts.",
    ]
    joke = random.choice(jokes)
    speak(joke)
    print(joke)

# Feature: Time
def get_time():
    """Tells the current time."""
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")
    print(f"The time is {strTime}")

# Feature: Date
def get_date():
    """Tells the current date."""
    strDate = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {strDate}")
    print(f"Today's date is {strDate}")
def get_name():
    speak(f"My name is  Eva")
    print(f"My name is  Eva")
# Feature: Calculate
def calculate(command):
    """Calculates the result of a mathematical expression."""
    try:
        expression = command.replace("calculate", "").strip()
        result = eval(expression)
        speak(f"The result is {result}")
        print(f"The result is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that.")
        logging.error(f"Calculation error: {e}")

# News Update Function
def get_news():
    """Fetches and speaks the top 5 news headlines."""
    try:
        api_key = "9d95bd32740b4001a41775b94f23ec3f"  # Replace with your News API key
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()
        articles = data["articles"]
        print("Here are the top news headlines:")
        speak("Here are the top news headlines.")
        for i, article in enumerate(articles[:5]):
            title = article["title"]
            description = article["description"]
            print(f"{i+1}. {title} - {description}")
            speak(f"{i+1}. {title}")
    except Exception as e:
        print(f"Failed to fetch news: {e}")
        speak("Sorry, I couldn't fetch the news.")
# Feature: Play Music
def play_music():
    """Plays random music from a predefined music folder."""
    music_dir = r"C:\Users\Raghu\Desktop\music"  # Use raw string to avoid Unicode errors
    try:
        songs = os.listdir(music_dir)  # Get all files in the music folder
        if songs:
            song_to_play = random.choice(songs)  # Choose a random song
            song_path = os.path.join(music_dir, song_to_play)
            os.startfile(song_path)  # Open the song file
            speak(f"Playing music")
        else:
            speak("Your music folder is empty. Please add some songs.")
    except Exception as e:
        speak("Sorry, I couldn't play music.")
        logging.error(f"Failed to play music: {e}")

# Main program
wish_me()
while True:
    query = takeCommand()
    if query:
        if "time" in query:
            get_time()
        elif "date" in query:
            get_date()
        elif "name" in query:
            get_name()
        elif "wikipedia" in query:
            search_wikipedia(query)
        elif "open" in query:
            open_application_or_website(query)
        elif "joke" in query:
            tell_joke()
        elif "calculate" in query:
            calculate(query)
        
        elif "news" in query:
            get_news()
        elif "music" in query:
            play_music()
        elif "song" in query:
            play_music()
        elif "exit" in query:
            speak("Goodbye, sir!")
            break
        else:
            speak("Sorry, I didn't understand that.")
