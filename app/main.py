from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import pandas as pd
from app import chatbot_backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (e.g., for favicon, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Favicon route
@app.get("/favicon.ico")
def favicon():
    return FileResponse("app/static/favicon.ico")

class Query(BaseModel):
    question: str

class Feedback(BaseModel):
    user_query: str
    matched_question: str
    answer: str
    feedback: str

@app.get("/")
def read_root():
    return {"message": "FAQ Chatbot API is running 🚀"}

@app.post("/ask")
def ask_question(query: Query):
    result = chatbot_backend.get_best_match(query.question)
    return result

@app.post("/feedback")
def submit_feedback(feedback: Feedback):
    chatbot_backend.log_feedback(feedback)
    return {"message": "Feedback recorded successfully."}

@app.get("/reload")
def reload_faq():
    chatbot_backend.reload_faq_data()
    return {"message": "FAQ dataset reloaded."}

@app.get("/categories", response_model=List[str])
def get_categories():
    df = pd.read_csv("app/data/faq_data.csv")
    categories = sorted(df["category"].dropna().unique().tolist())
    return categories
