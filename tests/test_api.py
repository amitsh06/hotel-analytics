import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_analytics_endpoint():
    response = client.post("/analytics")
    assert response.status_code == 200
    data = response.json()
    # Check that essential fields are present
    assert "total_bookings" in data
    assert "average_daily_rate" in data

def test_ask_endpoint_known_question():
    # Using a question we expect to match our predefined ones
    response = client.post("/ask", json={"text": "Show me total revenue for July 2017"})
    assert response.status_code == 200
    data = response.json()
    # You can set expected substrings in your answer, e.g., revenue format or context details
    assert "July 2017" in data["answer"]

def test_ask_endpoint_unknown_question():
    # Test with a question that is very different
    response = client.post("/ask", json={"text": "What is the weather like?"})
    assert response.status_code == 200
    data = response.json()
    # Expect a fallback answer if similarity is low
    assert "Based on our data:" in data["answer"]
