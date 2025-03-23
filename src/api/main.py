from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.analytics.reports import HotelAnalytics

app = FastAPI()
analytics = HotelAnalytics()

class Question(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Analytics API!"}

@app.post("/analytics")
def get_analytics():
    try:
        return analytics.generate_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_question(question: Question):
    try:
        return analytics.answer_question(question.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
