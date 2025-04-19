import os
import csv
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# File paths (Ensure these paths are correctly set relative to your project structure)
faq_path = "app/data/faq_data.csv"
unanswered_path = "app/data/unanswered_questions.csv"
feedback_log_path = "app/data/feedback_logs.csv"

# Load FAQ data
faq_df = pd.read_csv(faq_path)
faq_df.columns = faq_df.columns.str.lower()  # Normalize column names to lowercase
faq_df["question"] = faq_df["question"].fillna("")

# Globals
vectorizer = TfidfVectorizer()
faq_embeddings = None

# Reload FAQ data
def reload_faq_data():
    global faq_df, faq_embeddings, vectorizer

    if not os.path.exists(faq_path):
        faq_df = pd.DataFrame(columns=["question", "answer", "category"])
        faq_embeddings = None
        return

    faq_df = pd.read_csv(faq_path)
    faq_df.columns = faq_df.columns.str.lower()
    faq_df["question"] = faq_df["question"].fillna("")
    faq_embeddings = vectorizer.fit_transform(faq_df["question"])

# Load on start
reload_faq_data()

# Check if unanswered question and log it
def check_and_log_unanswered_question(user_query: str) -> bool:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_query_clean = user_query.strip().lower()

    # Create file if it doesn't exist
    if not os.path.exists(unanswered_path):
        with open(unanswered_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["user_query", "timestamp"])
            writer.writeheader()

    # Read and normalize existing queries
    existing_queries = set()
    try:
        with open(unanswered_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q = row.get("user_query", "").strip().lower()
                if q:
                    existing_queries.add(q)
    except Exception as e:
        print("Error reading unanswered_questions.csv:", e)

    # Check if already seen
    if user_query_clean in existing_queries:
        return True

    # If not, log it
    with open(unanswered_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([user_query, timestamp])

    return False

# Match user query to best FAQ
def get_best_match(user_query: str):
    global faq_df, faq_embeddings, vectorizer

    if faq_embeddings is None or faq_df.empty:
        return {
            "matched_question": None,
            "answer": "FAQ data not available.",
            "found": False
        }

    query_vec = vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vec, faq_embeddings).flatten()
    best_idx = similarities.argmax()
    score = similarities[best_idx]

    if score >= 0.4:
        matched_q = faq_df.iloc[best_idx]["question"]
        answer = faq_df.iloc[best_idx]["answer"]
        return {
            "matched_question": matched_q,
            "answer": answer,
            "found": True
        }
    else:
        already_seen = check_and_log_unanswered_question(user_query)
        if already_seen:
            return {
                "matched_question": None,
                "answer": "We've seen this question before and are working on it.",
                "found": False
            }
        else:
            return {
                "matched_question": None,
                "answer": "Sorry, I couldn't find a relevant answer. Your question has been logged for review.",
                "found": False
            }

# Feedback logging
def log_feedback(feedback):
    entry = {
        "user_query": feedback.user_query,
        "matched_question": feedback.matched_question,
        "answer": feedback.answer,
        "feedback": feedback.feedback,
        "timestamp": datetime.now().isoformat()
    }

    df = pd.DataFrame([entry])

    if not os.path.exists(feedback_log_path):
        df.to_csv(feedback_log_path, index=False)
    else:
        df.to_csv(feedback_log_path, mode="a", header=False, index=False)
