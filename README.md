# 🌟 WEDNESDAY – Virtual Assistant Model

**WEDNESDAY** is a desktop-based intelligent voice assistant powered by **Deep Learning (TensorFlow/Keras)** for Natural Language Understanding (NLU).  
It combines **offline reliability** with **online intelligence**, giving you a truly hybrid assistant that works seamlessly even without internet access.

---

## ✨ Features

### 🔹 **Hybrid Operation**
- Works **offline** for essential tasks (reminders, system control, and local knowledge base).  
- Uses the **internet** for advanced queries like web searches and Wikipedia lookups.

### 🧠 **ML-Powered NLU**
- Uses a trained **Keras model (`chat_model.h5`)** for high-accuracy **intent recognition**.  
- Understands diverse voice and text-based commands.

### 📘 **Offline Knowledge Base**
- Fast retrieval of factual information from a local dataset (`general_knowledge_qa.csv`).  
- Uses **semantic search** for context-aware question matching.

### ⚙️ **Task Automation**
- Perform desktop operations hands-free using commands like:
  - “Open Calculator”
  - “Increase volume”
  - “Take a screenshot”
- Built with `pyautogui` and `os` libraries for smooth automation.

### ⚡ **Caching**
- Implements a **search caching system (`search_cache.json`)** to:
  - Minimize repeated API calls
  - Increase web response speed

---

🛠️ Installation & Setup

Follow these steps to set up and run Wednesday on your system.

### 1️⃣ **Clone the Repository**

bash
git clone https://github.com/SamarthSehgal/WEDNESDAY---Virtual-Assistant-Model.git
cd WEDNESDAY---Virtual-Assistant-Model

### 2️⃣ **Create a Virtual Environment (Recommended)**
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

### 3️⃣ **Install Dependencies**

Install all required libraries listed in the requirements.txt file:

pip install -r requirements.txt

If the file is missing, manually install the core dependencies (listed below in Section II).

### 4️⃣ **Load the ML Model**

Ensure these files are placed in the project root directory:
chat_model.h5
tokenizer.pkl
label_encoder.pkl

These files are required for natural language understanding and intent classification.

### 5️⃣ **Run the Assistant**
python main.py

For the text-based version, use:
python main_text.py

### 🧩 **Project Structure**
WEDNESDAY---Virtual-Assistant-Model/
│
├── main.py                  # Voice-based assistant
├── main_text.py             # Text-based console assistant
├── intents.json             # Intent training data
├── chat_model.h5            # Trained NLU model
├── tokenizer.pkl            # Tokenizer for preprocessing
├── label_encoder.pkl        # Label encoder for class mapping
├── knowledge_base.py        # Offline knowledge retrieval system
├── internet_search_ddg.py   # Web search using DuckDuckGo API
├── general_knowledge_qa.csv # Local dataset for knowledge base
├── search_cache.json        # Caching for repeated searches
├── logs/                    # Interaction logs generated automatically
└── README.md                # Project documentation

### 💾 **Logging & Debugging**

All assistant interactions are logged in:
logs/assistant_log.txt

Each entry records:
1.User input
2.Intent classification & confidence score
3.Knowledge base & semantic similarity scores
4.Final decision path (Intent / KB / Web)
5.Timestamped response

### 👨‍💻 **Author**

Samarth Sehgal
