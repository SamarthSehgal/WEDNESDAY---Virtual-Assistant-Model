import json
import pickle
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# Load dataset
with open("intents.json") as file:
    data = json.load(file)

training_sentences = []
training_labels = []
labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        training_sentences.append(pattern)
        training_labels.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])


# Encode labels
label_encoder = LabelEncoder()
training_labels = label_encoder.fit_transform(training_labels)

# Tokenization
vocab_size = 2000
max_len = 20
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)

sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)


# Train/Validation Split
X_train, X_val, y_train, y_val = train_test_split(
    padded_sequences,
    training_labels,
    test_size=0.2,
    random_state=42
)


# Model Architecture Upgrade
model = Sequential([
    Embedding(vocab_size, 32, input_length=max_len),
    GlobalAveragePooling1D(),
    Dense(64, activation="relu"),
    Dropout(0.3),
    BatchNormalization(),
    Dense(32, activation="relu"),
    Dropout(0.3),
    Dense(len(labels), activation="softmax")
])

model.compile(loss='sparse_categorical_crossentropy', optimizer="adam", metrics=["accuracy"])
model.summary()


# Early Stopping to avoid overfitting
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)


# Train model
history = model.fit(
    X_train,
    y_train,
    epochs=300,
    validation_data=(X_val, y_val),
    callbacks=[early_stop]
)


# Save model & preprocessing files
model.save("chat_model.h5")
print("✅ Model Saved!")

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Tokenizer & Label Encoder Saved!")


# Plot Accuracy/Loss Graph
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(["Train", "Validation"])

plt.subplot(1,2,2)
plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend(["Train", "Validation"])

plt.tight_layout()
plt.show()
