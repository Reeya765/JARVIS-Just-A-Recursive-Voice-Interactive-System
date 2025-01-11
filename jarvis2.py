import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pygame
import time  # Importing time for reminders
import requests  # Importing requests to make HTTP requests

# Initialize text to speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

API_KEY = '32691905f10bd8b2054aee6da28e9869'  # Replace with your OpenWeatherMap API Key


def speak(audio):
    """
    This function will speak the string passed to it.
    """
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    """
    This function wishes the user based on the current time.
    """
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How may I assist you?")


def take_command():
    """
    This function takes microphone input from the user and returns string output.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.5
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Sorry, I couldn't understand that. Can you please repeat?")
        return "None"
    return query


def play_favorite_song(song_path):
    """
    This function plays the user's favorite song.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()


def calculate(query):
    """
    This function performs basic arithmetic operations.
    """
    try:
        result = eval(query)
        speak(f"The result is {result}.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't perform the calculation.")


def reverse_string(string):
    """
    This function reverses the given string.
    """
    return string[::-1]


def convert_units(value, from_unit, to_unit):
    """
    This function converts units between kilometers and miles.
    """
    if from_unit == "kilometers" and to_unit == "miles":
        return value * 0.621371
    elif from_unit == "miles" and to_unit == "kilometers":
        return value / 0.621371
    else:
        return None


def take_note():
    """
    This function allows the user to take notes and save them to a text file.
    """
    speak("What would you like to note down?")
    note = take_command()
    with open("notes.txt", "a") as file:
        file.write(note + "\n")
    speak("Note saved.")


def set_reminder():
    """
    This function sets a reminder for a specified duration.
    """
    speak("What time in seconds do you want to set the reminder for?")
    seconds = int(take_command())
    speak(f"Setting a reminder for {seconds} seconds.")
    time.sleep(seconds)
    speak("Reminder! Time's up!")


def get_random_quote():
    """
    This function returns a random motivational quote.
    """
    quotes = [
        "Keep your face always toward the sunshine—and shadows will fall behind you.",
        "The best way to predict the future is to create it.",
        "You are never too old to set another goal or to dream a new dream.",
        "Believe you can and you're halfway there.",
        "The only way to do great work is to love what you do."
    ]
    return quotes[0]  # Just returning the first quote for simplicity


def get_weather():
    """
    This function fetches the current weather for Pune.
    """
    city = "Pune"  # Hard-coding the city to Pune
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={API_KEY}&units=metric"  # Using metric for Celsius
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temperature = main["temp"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found.")



if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif 'search on google' in query:
            speak("What do you want to search for?")
            search_query = take_command()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif 'play music' in query:
            speak("Sure! What's the name of your favorite music?")
            music_name = take_command()
            search_query = music_name + " official audio"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        elif 'open pictures' in query:
            folder_path = r"C:\Users\Hrugved sangle\Pictures"  # Change to your folder path
            try:
                os.startfile(folder_path)
                speak("Opening your pictures folder.")
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open the folder.")

        elif 'open calculator' in query:
            try:
                os.startfile("calc.exe")
                speak("Opening the calculator.")
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open the calculator.")

        elif 'calculate' in query:
            speak("What calculation would you like to perform?")
            math_query = take_command().lower()
            calculate(math_query)

        elif 'reverse' in query:
            speak("What string would you like to reverse?")
            string_to_reverse = take_command().lower()
            reversed_string = reverse_string(string_to_reverse)
            speak(f"The reversed string is: {reversed_string}")

        elif 'convert' in query:
            speak("What value and unit do you want to convert?")
            conversion_query = take_command().lower()
            parts = conversion_query.split()
            if len(parts) == 4 and parts[1] in ["kilometers", "miles"] and parts[3] in ["kilometers", "miles"]:
                value = float(parts[0])
                from_unit = parts[1]
                to_unit = parts[3]
                result = convert_units(value, from_unit, to_unit)
                if result is not None:
                    speak(f"{value} {from_unit} is {result} {to_unit}.")
                else:
                    speak("Sorry, I cannot perform that conversion.")
            else:
                speak("Please specify the value and units correctly.")

        elif 'take note' in query:
            take_note()

        elif 'set reminder' in query:
            set_reminder()

        elif 'quote' in query:
            quote = get_random_quote()
            speak(quote)

        elif 'weather' in query:
               
               get_weather()

        elif 'quit' in query or 'exit' in query:
            speak("Goodbye!")
            break

        else:
            speak("I'm sorry, I didn't understand that.")