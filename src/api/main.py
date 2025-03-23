from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.analytics.reports import HotelAnalytics
import time
import psutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.error(f"Error in analytics endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_question(question: Question):
    try:
        return analytics.answer_question(question.text)
    except Exception as e:
        logger.error(f"Error in ask endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the system is functioning correctly.
    Checks system resources, API status, and returns performance metrics.
    
    Returns:
        Dict: System health information
    """
    try:
        # System metrics
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # API status
        status = "healthy"
        
        # Check if analytics module is working
        analytics_working = hasattr(analytics, "df") and len(analytics.df) > 0
        
        # Get performance metrics
        performance = analytics.get_performance_metrics() if hasattr(analytics, "get_performance_metrics") else {}
        
        return {
            "status": status,
            "timestamp": time.time(),
            "system": {
                "cpu_usage_percent": cpu_usage,
                "memory_usage_percent": memory_usage,
                "disk_usage_percent": disk_usage
            },
            "components": {
                "analytics_engine": "healthy" if analytics_working else "degraded",
                "database": "healthy",  # Placeholder for actual DB check
                "llm_service": "healthy"  # Placeholder for actual LLM check
            },
            "performance": performance
        }
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": time.time()
        }
