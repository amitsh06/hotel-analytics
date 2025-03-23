# 🏨 Hotel Analytics & Q&A System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) 
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Pandas](https://img.shields.io/badge/Pandas-2.2-yellow)
![License](https://img.shields.io/badge/License-MIT-purple)

> An intelligent system that processes hotel booking data, generates analytics insights, and answers natural language questions using advanced RAG techniques.

## 🌟 Project Overview

This system is designed to transform raw hotel booking data into actionable insights through:

- **Advanced Data Preprocessing** - Cleaning and structuring raw booking data
- **Comprehensive Analytics** - Generating key business metrics and visualizations
- **Natural Language Q&A** - Answering questions about the data using RAG approach
- **Modern API** - Exposing functionality through a well-designed REST API
- **System Monitoring** - Health check endpoints with resource monitoring

## ✨ Features

### 📊 Data Preprocessing
Transforms messy hotel booking data into clean, structured datasets:
- Handles missing values and outliers
- Computes derived metrics (total nights, revenue, etc.)
- Prepares data for analytics and RAG processing

### 📈 Analytics Reporting
Generates comprehensive business insights including:
- Total bookings and occupancy rates
- Average daily rate and revenue analysis
- Cancellation patterns and trends
- Geographic distribution of guests
- Booking lead time and seasonality metrics

### 🔍 Retrieval-Augmented Q&A
Combines vector search with structured data analysis:
- FAISS-powered vector similarity search
- SentenceTransformer embedding for semantic understanding
- Custom logic for handling specific query types
- Natural language responses to business questions

### 🚀 REST API
Modern FastAPI implementation with:
- **POST /analytics:** Comprehensive analytics dashboard data
- **POST /ask:** Natural language Q&A endpoint
- **GET /health:** System health monitoring with resource metrics
- Swagger UI documentation
- Optimized for performance

### 🔄 System Monitoring
Real-time system health monitoring:
- CPU, memory, and disk usage tracking using psutil
- Component status monitoring (analytics engine, database, LLM)
- Performance metrics collection and reporting
- Graceful error handling and reporting

## 🏗️ Project Structure

```
hotel-analytics/
├── src/
│   ├── api/              # FastAPI implementation
│   │   └── main.py       # Main API with endpoints including health check
│   ├── analytics/        # Analytics & vector store
│   │   └── reports.py    # Data analysis and reporting logic
│   └── data/             # Data processing modules
│       └── processed/    # Processed data files
├── tests/                # Automated testing
├── documentation/
│   ├── api_documentation.md      # API endpoints documentation
│   ├── llm_integration.md        # LLM integration details
│   ├── documentation.md          # Health check documentation
│   └── manual_tests.md           # Manual test cases
├── test_functionality.py         # Basic functionality test script
├── IMPLEMENTATION_REPORT.md      # Implementation details
├── IMPLEMENTATION_REPORT_UPDATES.md # Updates to implementation
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/amitsh06/hotel-analytics.git
   cd hotel-analytics
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Data Preprocessing

```bash
python src/data/preprocessing.py
```

### Starting the API Server

```bash
uvicorn src.api.main:app --reload
```

The API will be available at:
- 🌐 API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📚 Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### API Endpoints

#### Analytics Dashboard
```http
POST /analytics
```
Returns comprehensive analytics metrics and visualizations.

**Example Response:**
```json
{
  "total_bookings": 119390,
  "average_daily_rate": 101.83,
  "cancellation_rate": 0.37,
  "revenue_trends": {
    "2016-01": 980450.32,
    "2016-02": 1054783.45,
    // More months...
  },
  "geographical_distribution": {
    "Portugal": 48951,
    "UK": 12563,
    // More countries...
  },
  "lead_time_stats": {
    "mean": 104.5,
    "median": 72,
    "min": 0,
    "max": 737
  }
}
```

#### Question Answering
```http
POST /ask
Content-Type: application/json

{
  "question": "What was the revenue from Portugal bookings in August 2017?"
}
```

**Example Response:**
```json
{
  "answer": "The total revenue from Portugal bookings in August 2017 was €243,512.75",
  "confidence": 0.92,
  "relevant_data": {
    "month": "August",
    "year": 2017,
    "country": "Portugal",
    "booking_count": 2341,
    "revenue": 243512.75
  }
}
```

#### Health Check
```http
GET /health
```
Returns system health information and resource metrics.

**Example Response:**
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
    "avg_response_time_seconds": 0.125,
    "successful_queries": 42,
    "failed_queries": 2,
    "total_queries": 44
  }
}
```

## 🧪 Testing & Performance

Run automated tests:
```bash
python -m pytest tests/
```

## 🔬 System Outputs & Results

This repository includes real outputs from the system during testing, stored in the `outputs/` directory. These JSON files show actual results from running the system and can be examined to verify functionality:

- `outputs/analytics_report.json` - Complete analytics dashboard data
- `outputs/sample_queries/` - Various question-answer pairs showing RAG functionality
- `outputs/performance_metrics.json` - System performance measurements

These outputs demonstrate that:
1. The analytics engine correctly processes and summarizes booking data
2. The Q&A system successfully answers natural language questions about the data
3. The system meets performance requirements for response time and accuracy

## 📑 Implementation Report

A detailed implementation report is available in [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md), covering:
- System architecture and component design
- Implementation choices and rationale
- Technical challenges and solutions
- Sample test queries with expected outputs
- Future improvement opportunities

## 📦 Deployment Options

- **Docker:** Container-based deployment
- **Cloud Services:** AWS, Azure, GCP
- **PaaS:** Heroku, Railway, Render

## 🔄 Continuous Improvement

Planned enhancements:
- Real-time data updates
- Advanced visualization capabilities
- Multi-language support
- Expanded machine learning features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

Built with powerful open-source technologies:
- [FastAPI](https://fastapi.tiangolo.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [SentenceTransformer](https://www.sbert.net/)
- [Pandas](https://pandas.pydata.org/)

---

<p align="center">
  <b>Made with ❤️ by Amit Sharma</b>
</p>
