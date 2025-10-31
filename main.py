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
import re
from sentence_transformers import SentenceTransformer, util
from knowledge_base import query_knowledge_base
from internet_search_ddg import search_duckduckgo
from nltk.wsd import lesk
import nltk
from nltk.tokenize import word_tokenize

# ------------------ NLTK Setup ------------------
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('punkt', quiet=True)

# ------------------ Load Model & Data ------------------
with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

# ------------------ Load Semantic Model ------------------
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# ------------------ Voice Engine ------------------
def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    print(f"Wednesday: {text}")
    engine.say(text)
    engine.runAndWait()

# ------------------ Logging ------------------
def log_interaction(user_query, intent_tag, confidence, threshold, kb_score, sem_score, weight, decision, response):
    """Append structured logs for debugging and fine-tuning."""
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = os.path.join("logs", "assistant_log.txt")

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}]\n")
        log.write(f"USER: {user_query}\n")
        log.write(f"INTENT: {intent_tag} | Confidence: {confidence:.2f} | Threshold: {threshold:.2f}\n")
        log.write(f"KB_SCORE: {kb_score:.2f} | SEM_SCORE: {sem_score:.2f} | WEIGHT: {weight:.2f}\n")
        log.write(f"DECISION: {decision}\n")
        log.write(f"RESPONSE: {response}\n")
        log.write("-" * 70 + "\n")

# ------------------ Voice Input ------------------
def command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("🎧 Listening...", end="", flush=True)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("\r⏳ No speech detected.")
                return None
    except OSError:
        print("🎙️ Microphone not detected.")
        speak("No microphone found, please check your audio input device.")
        return None

    try:
        print("\r🤔 Recognizing...", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print(f"\r🗣️ You said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("❌ I didn’t catch that.")
        return None
    except sr.RequestError:
        print("⚠️ Network error while recognizing speech.")
        return None

# ------------------ Lesk Context Extraction ------------------
def extract_contextual_meaning(sentence):
    words = word_tokenize(sentence)
    senses = {}
    for word in words:
        synset = lesk(words, word)
        if synset:
            senses[word] = synset.definition()
    if senses:
        print(f"🔍 Contextual senses extracted for {len(senses)} words.")
    return senses

# ------------------ Utility Functions ------------------
def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict = {1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}
    return day_dict.get(day, "Unknown")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = cal_day()
    if hour < 12:
        speak(f"Good morning, it's {day} and the time is {t}")
    elif hour < 16:
        speak(f"Good afternoon, it's {day} and the time is {t}")
    else:
        speak(f"Good evening, it's {day} and the time is {t}")

# ------------------ Functional Commands ------------------
def social_media(query):
    sites = {'facebook':"https://www.facebook.com/",'discord':"https://discord.com/",'whatsapp':"https://web.whatsapp.com/",'instagram':"https://www.instagram.com/",'youtube':"https://www.youtube.com/"}
    for key, url in sites.items():
        if key in query.lower():
            speak(f"Opening {key.capitalize()}")
            webbrowser.open(url)
            return
    speak("No Result Found")

def openApp(query):
    if "calculator" in query.lower():
        speak("Opening calculator"); os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in query.lower():
        speak("Opening notepad"); os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in query.lower():
        speak("Opening paint"); os.startfile('C:\\Windows\\System32\\mspaint.exe')

def closeApp(query):
    if "calculator" in query.lower():
        speak("Closing calculator"); os.system("taskkill /f /im calc.exe")
    elif "notepad" in query.lower():
        speak("Closing notepad"); os.system('taskkill /f /im notepad.exe')
    elif "paint" in query.lower():
        speak("Closing paint"); os.system('taskkill /f /im mspaint.exe')

def schedule():
    day = cal_day().lower()
    speak("Today's schedule is ")
    week = {
        "monday": "Sir, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 System Design, then Programming Lab after lunch.",
        "tuesday": "Sir, you have Web Development and Database Systems, followed by Open Source Lab in the afternoon.",
        "wednesday": "Sir, full day of classes — Mini Project, Cyber Security, Python, and AI/ML before lunch.",
        "thursday": "Sir, Computer Networks, Cloud Computing, and Cybersecurity Lab after lunch.",
        "friday": "Sir, AI, Advanced Programming, and UI/UX Design in the morning, followed by Capstone work.",
        "saturday": "Sir, meetings and personal project work today.",
        "sunday": "Sir, today is a holiday. Relax and recharge!"
    }
    if day in week:
        speak(week[day])
    else:
        speak("I couldn’t find today’s schedule.")

# ------------------ Main Program ------------------
if __name__ == "__main__":
    wishMe()
    speak("Hello, I'm Wednesday. How can I assist you today?")

    while True:
        query = command()
        if not query:
            continue

        # Step 1️⃣ — Context understanding (Lesk)
        senses = extract_contextual_meaning(query)

        # Step 2️⃣ — Handle functional commands
        if any(x in query for x in ['facebook','discord','whatsapp','instagram','youtube']):
            social_media(query); continue
        if "schedule" in query:
            schedule(); continue
        if "exit" in query or "quit" in query or "goodbye" in query:
            speak("Goodbye, have a great day!"); sys.exit()
        if "open" in query: openApp(query); continue
        if "close" in query: closeApp(query); continue
        if "volume up" in query: pyautogui.press("volumeup"); speak("Volume increased"); continue
        if "volume down" in query: pyautogui.press("volumedown"); speak("Volume decreased"); continue
        if "mute" in query: pyautogui.press("volumemute"); speak("Volume muted"); continue

        # Step 3️⃣ — Intent Model Prediction
                # -------- Intent Detection ----------

        # Predict raw probabilities
        padded = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
        raw_result = model.predict(padded)[0]
        # Softmax normalization for consistency
        probs = np.exp(raw_result) / np.sum(np.exp(raw_result))
        intent_index = np.argmax(probs)
        confidence = float(probs[intent_index])
        tag = label_encoder.inverse_transform([intent_index])[0]

        # Dynamic threshold adjustment
        length = len(query.split())
        if length <= 3:
            INTENT_CONF_THRESHOLD = 0.35   # small queries → more lenient
        elif length >= 10:
            INTENT_CONF_THRESHOLD = 0.70
        else:
            INTENT_CONF_THRESHOLD = 0.55

        print(f"🧠 Intent: {tag} | Confidence: {confidence:.2f} | Threshold: {INTENT_CONF_THRESHOLD:.2f}")

        smalltalk_tags = [
            "greeting","goodbye","thanks","jokes","Identity","whatsup",
            "haha","programmer","insult","activity","exclaim",
            "appreciate","nicetty","no","greetreply"
        ]

        kb_score = sem_score = KB_WEIGHT = 0.0
        decision = ""
        response_text = ""

        # ✅ Step 1 — Small-talk direct handling
        if tag in smalltalk_tags and confidence >= 0.25:
            for intent in data['intents']:
                if intent['tag'] == tag:
                    response_text = random.choice(intent['responses'])
                    speak(response_text)
                    decision = "Small-talk intent triggered"
                    break
            log_interaction(query, tag, confidence, INTENT_CONF_THRESHOLD, kb_score, sem_score, KB_WEIGHT, decision, response_text)
            continue

        # ✅ Step 2 — Confirm via semantic similarity (intent patterns)
        if confidence < INTENT_CONF_THRESHOLD:
            max_sim = 0.0
            best_tag = None
            q_emb = semantic_model.encode(query, convert_to_tensor=True)
            for intent in data['intents']:
                for pattern in intent["patterns"]:
                    p_emb = semantic_model.encode(pattern, convert_to_tensor=True)
                    sim = float(util.cos_sim(q_emb, p_emb))
                    if sim > max_sim:
                        max_sim, best_tag = sim, intent["tag"]

            if best_tag and max_sim >= 0.60:
                for intent in data['intents']:
                    if intent['tag'] == best_tag:
                        response_text = random.choice(intent['responses'])
                        speak(response_text)
                        decision = f"Semantic intent match ({best_tag})"
                        break
                log_interaction(query, best_tag, confidence, INTENT_CONF_THRESHOLD, kb_score, sem_score, KB_WEIGHT, decision, response_text)
                continue

        # ✅ Step 3 — Confident model match
        if confidence >= INTENT_CONF_THRESHOLD:
            for intent in data['intents']:
                if intent['tag'] == tag:
                    response_text = random.choice(intent['responses'])
                    speak(response_text)
                    decision = "Intent model confident"
                    break
            log_interaction(query, tag, confidence, INTENT_CONF_THRESHOLD, kb_score, sem_score, KB_WEIGHT, decision, response_text)
            continue

        # ❌ Low confidence → Knowledge Base or Web
        try:
            kb_results = query_knowledge_base(query, top_k=1)
            idx, score, kb_question, kb_answer = kb_results[0]

            q_emb = semantic_model.encode(query, convert_to_tensor=True)
            kb_emb = semantic_model.encode(kb_question, convert_to_tensor=True)
            sem_score = float(util.cos_sim(q_emb, kb_emb))
            KB_WEIGHT = (0.3 * score) + (0.7 * sem_score)
            answer_len = len(re.findall(r'\w+', kb_answer))

            print(f"📘 KB_SCORE={score:.2f} | SEM_SCORE={sem_score:.2f} | WEIGHT={KB_WEIGHT:.2f}")

            if sem_score >= 0.70 or (KB_WEIGHT >= 0.55 and answer_len > 5):
                response_text = f"According to my knowledge base: {kb_answer}"
                speak(response_text)
                decision = "Knowledge Base used"
                try:
                    web_check = search_duckduckgo(query)
                    if kb_answer.lower() not in web_check.lower() and sem_score < 0.80:
                        speak("That might not be completely accurate. Here's what I found online instead.")
                        speak(web_check)
                        decision = "Web verified KB answer"
                except Exception:
                    pass

            elif 0.40 <= sem_score < 0.70:
                speak("I found something similar in my knowledge base, but I'm not sure it's exact.")
                speak(f"Do you want me to read it? (yes or no)")
                choice = input(">> ").lower()
                if "y" in choice:
                    response_text = kb_answer
                    speak(kb_answer)
                    decision = "User confirmed KB answer"
                else:
                    speak("Let me check online for you.")
                    web_result = search_duckduckgo(query)
                    response_text = web_result
                    speak(f"Here's what I found: {web_result}")
                    decision = "User rejected KB, used Web"

            else:
                speak("Let me check online for you.")
                web_result = search_duckduckgo(query)
                response_text = web_result
                speak(f"Here's what I found: {web_result}")
                decision = "Low KB score, used Web"

        except Exception as e:
            print("⚠️ Knowledge base lookup failed:", e)
            try:
                web_result = search_duckduckgo(query)
                response_text = web_result
                speak(f"Here's what I found: {web_result}")
                decision = "KB failed, Web fallback"
            except Exception:
                response_text = "Offline mode: No web or KB access."
                speak("It seems there's no internet connection available.")
                speak("I'm limited to offline knowledge for now.")
                decision = "Offline fallback"

        # Log every decision
        log_interaction(query, tag, confidence, INTENT_CONF_THRESHOLD,
                        score if 'score' in locals() else 0.0,
                        sem_score if 'sem_score' in locals() else 0.0,
                        KB_WEIGHT if 'KB_WEIGHT' in locals() else 0.0,
                        decision, response_text)
