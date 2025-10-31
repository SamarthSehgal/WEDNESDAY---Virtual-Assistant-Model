import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

ARTIFACT_DIR = "kb_artifacts"

with open(f"{ARTIFACT_DIR}/kb_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open(f"{ARTIFACT_DIR}/kb_tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix = pickle.load(f)
with open(f"{ARTIFACT_DIR}/kb_questions.pkl", "rb") as f:
    questions = pickle.load(f)
with open(f"{ARTIFACT_DIR}/kb_answers.pkl", "rb") as f:
    answers = pickle.load(f)

def query_knowledge_base(query, top_k=3):
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, tfidf_matrix).flatten()
    top_idx = np.argsort(-sims)[:top_k]
    results = [(int(idx), float(sims[idx]), questions[idx], answers[idx]) for idx in top_idx]
    return results
