from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)

# Load models
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
sentiment_analyzer = pipeline("sentiment-analysis")

class NewsInput(BaseModel):
    content: str

@app.post("/analyze/")
def analyze_news(data: NewsInput):
    summary = summarizer(data.content, max_length=120, min_length=30, do_sample=False)[0]["summary_text"]
    sentiment = sentiment_analyzer(summary)[0]
    return {"summary": summary, "sentiment": sentiment}