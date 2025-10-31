import json
import pickle
import numpy as np
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from knowledge_base import query_knowledge_base
from internet_search_ddg import search_duckduckgo

# ---------------- Load Chatbot Model ----------------
with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

# ---------------- Interactive Loop ----------------
print("🤖 Wednesday is ready! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("👋 Goodbye!")
        break

    # ---------- Step 1: Predict intent ----------
    padded_seq = pad_sequences(tokenizer.texts_to_sequences([user_input]), maxlen=20, truncating="post")
    result = model.predict(padded_seq)
    intent_index = np.argmax(result)
    confidence = float(result[0][intent_index])
    tag = label_encoder.inverse_transform([intent_index])[0]

    INTENT_CONF_THRESHOLD = 0.60
    KB_CONF_THRESHOLD = 0.35

    # ---------- Step 2: Use chatbot response if confident ----------
    if confidence >= INTENT_CONF_THRESHOLD:
        for intent in data["intents"]:
            if intent["tag"] == tag:
                reply = np.random.choice(intent["responses"])
                print(f"Wednesday: {reply}")
                break

    # ---------- Step 3: Knowledge base fallback ----------
    else:
        try:
            kb_results = query_knowledge_base(user_input, top_k=1)
            idx, score, kb_question, kb_answer = kb_results[0]

            if score >= KB_CONF_THRESHOLD:
                print(f"Wednesday (KB): {kb_answer}")
            else:
                # ---------- Step 4: Online fallback ----------
                print("Wednesday: Let me check online for you...")
                web_result = search_duckduckgo(user_input)
                print(f"Wednesday (Web): {web_result}")

        except Exception as e:
            # ---------- Step 5: Handle KB errors gracefully ----------
            print("⚠️ Knowledge base lookup failed:", e)
            print("Wednesday: I'm having trouble with my knowledge base. Let me check online.")
            web_result = search_duckduckgo(user_input)
            print(f"Wednesday (Web): {web_result}")
