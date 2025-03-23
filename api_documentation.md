# Hotel Analytics System - API Documentation

## Overview
The Hotel Analytics API provides access to booking data analytics, report generation, and question-answering capabilities powered by a language model. The API is built using FastAPI and follows RESTful principles.

## Base URL
```
http://localhost:8000
```

## Endpoints

### Root Endpoint
```
GET /
```

Returns a welcome message to confirm the API is running.

**Response:**
```json
{
  "message": "Welcome to the Hotel Analytics API!"
}
```

### Analytics Endpoint
```
POST /analytics
```

Generates a comprehensive analytics report about hotel bookings.

**Request:**
No request body required.

**Response:**
```json
{
  "booking_summary": {
    "total_bookings": 119390,
    "resort_hotel_bookings": 79330,
    "city_hotel_bookings": 40060,
    "cancellation_rate": 37.0,
    "average_lead_time": 104.0
  },
  "seasonal_analysis": {
    "peak_month": "August",
    "low_season": ["January", "December"],
    "weekend_vs_weekday": {
      "weekend_bookings_percent": 27.5,
      "weekday_bookings_percent": 72.5
    }
  },
  "guest_demographics": {
    "top_countries": ["Portugal", "UK", "France", "Spain", "Germany"],
    "family_vs_individual": {
      "family_bookings_percent": 22.5,
      "individual_bookings_percent": 77.5
    }
  },
  "financial_insights": {
    "average_daily_rate": "$100.75",
    "revenue_by_hotel_type": {
      "resort_hotel": "$4,952,376",
      "city_hotel": "$6,180,590"
    },
    "deposit_type_distribution": {
      "no_deposit": 86.5,
      "non_refund": 8.5,
      "refundable": 5.0
    }
  }
}
```

### Ask Endpoint
```
POST /ask
```

Answers natural language questions about the hotel booking data using an LLM.

**Request:**
```json
{
  "text": "What is the average daily rate for hotel bookings?"
}
```

**Response:**
```json
{
  "answer": "The average daily rate (ADR) for hotel bookings is $100.75. This rate is higher in city hotels ($103.80) compared to resort hotels ($98.40).",
  "confidence": 0.92,
  "sources": ["adr_analysis", "hotel_type_comparison"]
}
```

### Health Endpoint
```
GET /health
```

Provides health status and performance metrics for the system.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1692725956.9512255,
  "system": {
    "cpu_usage_percent": 17.9,
    "memory_usage_percent": 83.3,
    "disk_usage_percent": 67.6
  },
  "components": {
    "analytics_engine": "healthy",
    "database": "healthy",
    "llm_service": "healthy"
  },
  "performance": {
    "avg_response_time_seconds": 0,
    "successful_queries": 0,
    "failed_queries": 0,
    "total_queries": 0
  }
}
```

## Testing with curl

### Test Root Endpoint
```bash
curl -X GET http://localhost:8000/
```

### Test Analytics Endpoint
```bash
curl -X POST http://localhost:8000/analytics
```

### Test Ask Endpoint
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the average daily rate for hotel bookings?"}'
```

### Test Health Endpoint
```bash
curl -X GET http://localhost:8000/health
```

## Testing with PowerShell

### Test Root Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Test Analytics Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/analytics" -Method POST -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Test Ask Endpoint
```powershell
$body = @{
    text = "What is the average daily rate for hotel bookings?"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/ask" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing | Select-Object -ExpandProperty Content
```

### Test Health Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing | Select-Object -ExpandProperty Content
```

## Error Responses

The API returns standard HTTP status codes along with a JSON response containing error details:

**400 Bad Request**
```json
{
  "detail": "Invalid request format"
}
```

**404 Not Found**
```json
{
  "detail": "Resource not found"
}
```

**500 Internal Server Error**
```json
{
  "detail": "An unexpected error occurred"
}
``` 