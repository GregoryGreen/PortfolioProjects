import ssl
from typing import Text
import wolframalpha
from PyDictionary import PyDictionary as Diction
import datetime
import os
from os import link, name, replace
from bs4 import BeautifulSoup
import pyttsx3
from pywhatkit.main import search
import requests
import speech_recognition as sr
import webbrowser
import pywhatkit as kit
import wikipedia
from gtts import gTTS
import translators as ts
ssl._create_default_https_context = ssl._create_unverified_context

Assistant = pyttsx3.init()
voices = Assistant.getProperty('voices')
print(voices)
Assistant.setProperty('voices', voices[0].id)
Assistant.setProperty('rate', 200)


def Speak(audio):
    print("  ")
    Assistant.say(audio)
    print(f": {audio}")
    print("  ")
    Assistant.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        Speak("Good morning")
    if hour > 12 and hour < 18:
        Speak("Good afternoon")
    else:
        Speak("Good Evening")
    Speak("I am Jarvis. How can I be of assistance?")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-us')
            print(f"You said: {query}")
        except sr.UnknownValueError:
            Speak("Sorry I did not get that.")
            return "none"
        return query.lower()


def TaskExe():
    while True:
        query = takecommand()

        if 'how are you' in query.lower():
            Speak("I am fine!")
            Speak("What about you?")
        elif 'You need a break' in query:
            Speak("Ok, You can call me anytime!")
        elif 'bye' in query.lower():
            Speak("Ok, bye!")
            break
        elif 'youtube search' in query.lower():
            Speak("Searching youtube...")
            query = query.replace("youtube search", "")
            result = kit.playonyt(query)
            print(result)
        elif 'website' in query.lower():
            Speak("Tell me the name of the website.")
            name = takecommand()
            web = 'https://www.' + name + '.com'
            webbrowser.open(web)
        elif 'wikipedia' in query.lower():
            Speak("Searching wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            Speak(result)
        elif 'google search' in query.lower():
            import wikipedia as googleScrap
            query = query.replace("jarvis", "")
            query = query.replace("google search", "")
            query = query.replace("google map", "")
            Speak("This is what I found on the web!")
            kit.search(query)
            try:
                result = googleScrap.summary(query, 2)
                Speak(result)
            except:
                Speak("No speakable data available!")
        elif 'translator' in query.lower():
            Speak("What do you want to translate?")
            say = takecommand()
            text = f"{say}"
            # translate english to Spanish
            print(ts.google(text, from_language='en', to_language='es'))
            Speak(ts.google(text, from_language='en', to_language='es'))

        elif 'temperature' in query.lower():
            query = query.replace("temperature", "")
            search = f"temperaure in {query}"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temperature = data.find("div", class_="BNeawe").text
            temperature2 = data.find("div", class_="BNeawe tAd8D AP7Wnd").text
            Speak(f"The temperature is {temperature}, {temperature2}.")

        elif 'time' in query.lower():
            query = query.replace("time", "")
            search = f"time in {query}"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            time = data.find("div", class_="BNeawe").text
            Speak(f"The time is {time}.")

        elif 'where is' in query.lower():
            query = query.replace("where is", "")
            Speak(f"{query}")
            url = "https://www.google.nl/maps/place/" + query + "/&amp;"
            webbrowser.get().open(url)

        elif 'calculate' in query.lower():
            Speak("What do you want to calculate? Example: 5 plus 4.")
            question = takecommand()
            app_id = "7GTV4H-T2LEYKT4JP"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            Speak("The answer is " + answer)


wish()
takecommand()
TaskExe()
