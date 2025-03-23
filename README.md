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
- Swagger UI documentation
- Optimized for performance

## 🏗️ Project Structure

```
hotel-analytics/
├── src/
│   ├── api/              # FastAPI implementation
│   ├── analytics/        # Analytics & vector store
│   └── data/             # Data processing modules
├── tests/                # Automated testing
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

#### Question Answering
```http
POST /ask
Content-Type: application/json

{
  "question": "What was the revenue from Portugal bookings in August 2017?"
}
```

## 🧪 Testing & Performance

Run automated tests:
```bash
python -m pytest tests/
```

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
