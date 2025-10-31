# kb_rebuild.py
import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def rebuild_kb(csv_path="general_knowledge_qa.csv", output_dir="kb_artifacts"):
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    if "question" not in df.columns or "answer" not in df.columns:
        print("❌ CSV must have columns 'question' and 'answer'")
        return

    questions = df["question"].fillna("").astype(str).tolist()
    answers = df["answer"].fillna("").astype(str).tolist()

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(questions)

    # Save artifacts
    with open(os.path.join(output_dir, "kb_vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
    with open(os.path.join(output_dir, "kb_questions.pkl"), "wb") as f:
        pickle.dump(questions, f)
    with open(os.path.join(output_dir, "kb_answers.pkl"), "wb") as f:
        pickle.dump(answers, f)
    with open(os.path.join(output_dir, "kb_tfidf_matrix.pkl"), "wb") as f:
        pickle.dump(tfidf_matrix, f)

    print(f"✅ Knowledge base rebuilt with {len(questions)} Q&A pairs.")

if __name__ == "__main__":
    rebuild_kb()
