import keras
import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model 
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil 
import subprocess
from sentence_transformers import SentenceTransformer, util
import re



with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("🎧 Listening...", end="", flush=True)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("\r⏳ No speech detected. Listening timed out.")
            return None

    try:
        print("\r🤔 Recognizing...", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print(f"\r🗣️ You said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("❌ I didn’t catch that. Could you repeat?")
        return None
    except sr.RequestError:
        print("⚠️ Network error while recognizing speech.")
        return None


def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning, it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon, it's {day} and the time is {t}")
    else:
        speak(f"Good evening, it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'discord' in command:
        speak("Opening Discord")
        webbrowser.open("https://discord.com/")
    elif 'whatsapp' in command:
        speak("Opening Whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'instagram' in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com/")
    elif 'youtube' in command:
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com/")
    else: 
        speak("No Result Found")


def schedule():
    day = cal_day().lower()
    speak("Today's schedule is ")
    week={
    "monday": "Sir, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
    "tuesday": "Sir, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
    "wednesday": "Sir, today you have a full day of classes. From 9:30 to 10:15 you have Mini Project class, from 10:15 to 11:15 you have Cyber Security class, from 11:15 to 12:15 you have Python class, from 12:15 to 1:15 you have AI/ML class, and from 1:15 to 2:15 you have a break.",
    "thursday": "Sir, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
    "friday": "Sir, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
    "saturday": "Sir, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
    "sunday": "Sir, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("opening paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im calc.exe")
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')

def browsing(query):
    if 'google' in query:
        speak("What should i search on google..")
        s = command().lower()
        webbrowser.open(f"{s}")

if __name__ == "__main__":
    wishMe()
    # engine_talk("Allow me to introduce myself I am Wednesday, the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can, 24 hours a day seven days a week.")
    while True:
        
        query = command().lower()
        #query  = input("Enter your command-> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query) or ('youtube' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decrease")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif ('pause' in query) or ('pause the video' in query):
            pyautogui.press("space")
        elif ('play' in query) or ('play the video' in query):
            pyautogui.press("space")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)
        elif ('exit' in query) or ('quit' in query) or ('exit the program' in query):
            sys.exit()
        elif any(word in query for word in ["what", "who", "how", "why", "where", "when"]):
    # Predict using trained chatbot model
         padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
         result = model.predict(padded_sequences)
         intent_index = np.argmax(result)
         confidence = float(result[0][intent_index])
         tag = label_encoder.inverse_transform([intent_index])[0]

         INTENT_CONF_THRESHOLD = 0.60  # threshold for intent model confidence

         if confidence >= INTENT_CONF_THRESHOLD:
        # High-confidence intent: use chatbot response
          for intent in data['intents']:
            if intent['tag'] == tag:
                speak(np.random.choice(intent['responses']))
                break

        else:
        # Low-confidence: try Knowledge Base, else fallback to DuckDuckGo
         from knowledge_base import query_knowledge_base
         from internet_search_ddg import search_duckduckgo

        try:
            # Try local KB
            kb_results = query_knowledge_base(query, top_k=1)
            idx, score, kb_question, kb_answer = kb_results[0]

            if score >= 0.45 and len(kb_answer.split()) > 5:
             speak(f"According to my knowledge base: {kb_answer}")
            else:
             speak("Let me check online for you.")
            web_result = search_duckduckgo(query)
            speak(f"Here's what I found: {web_result}")

        except Exception as e:
            # Handle missing KB or any errors gracefully
            print("⚠️ Knowledge base lookup failed:", e)
            speak("I'm having trouble accessing my knowledge base. Let me check online.")
            web_result = search_duckduckgo(query)
            speak(f"Here's what I found: {web_result}")


        # speak("Hello, I'm WEDNESDAY")