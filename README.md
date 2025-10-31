🌟 WEDNESDAY - Virtual-Assistant-Model
WEDNESDAY is a desktop-based voice assistant that uses a Deep Learning model (TensorFlow/Keras) for Natural Language Understanding (NLU). Its core innovation is a hybrid architecture that provides reliable, hands-free functionality even without an internet connection.

Creating a good GitHub repository (repo) is key to showcasing your project. It needs a detailed README file that tells visitors exactly what the project is, how it works, and how to set it up.

✨ Features
Hybrid Operation: Core features (reminders, system control, local knowledge base) run offline, while complex queries (web searches, Wikipedia lookups) utilize the internet.

ML-Powered NLU: Uses a trained Keras model (chat_model.h5) for high-accuracy Intent Recognition to understand diverse user commands.

Offline Knowledge Base: Fast retrieval of internal, factual answers from a local knowledge base (general_knowledge_qa.csv).

Task Automation: Utilizes voice commands to open applications and perform system tasks using libraries like pyautogui.

Caching: Implements a search caching mechanism (search_cache.json) to minimize repeat API calls and speed up responses.

🛠️ Installation & Setup
To run WEDNESDAY locally, follow these steps:

1. Clone the Repository:
   
git clone [Your GitHub Link Here]
cd WEDNESDAY-VoiceAssistant

2. Create a Virtual Environment (Recommended):

python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3. Install Dependencies: Install all required libraries listed in the requirements.txt file (see Section II).

pip install -r requirements.txt

4. Load the ML Model: Ensure the trained model (chat_model.h5) and serialization files (tokenizer.pkl, label_encoder.pkl) are present in the project root.

5. Run the Assistant:

python main.py

II. Additional Essential Repository Files
These files provide essential context and configuration for anyone using or reviewing your code.

This file lists the exact dependencies needed to recreate your environment(file included):

# Core I/O
speechrecognition
pyttsx3
pyaudio

# ML/NLU Core
tensorflow
numpy
sentence-transformers
scikit-learn # Needed for label_encoder

# Utilities & Data
json
datetime
pyautogui
webbrowser
wikipedia
requests

# Note: pyaudio may require system-level installation of portaudio on some systems (e.g., 'brew install portaudio' on macOS).

