import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.analytics.vector_store import VectorStore
import logging
import time
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HotelAnalytics:
    def __init__(self):
        try:
            # Load the processed CSV file
            file_path = r"C:\Users\maith\OneDrive - Manipal University Jaipur\Desktop\hotel analytics\src\data\processed\hotel_bookings_processed.csv"
            self.df = pd.read_csv(file_path)
            
            # Create a summary column to be indexed by the vector store.
            # This provides context for the LLM to generate better answers
            self.df['summary'] = self.df.apply(
                lambda row: (f"Booking from {row['country']} in {row['arrival_date_month']} {row['arrival_date_year']} "
                            f"with daily rate ${row['adr']} for {row['total_nights']} nights. "
                            f"Total price: ${row['total_price']}. "
                            f"Booking was {'canceled' if row['is_canceled'] == 1 else 'not canceled'}. "
                            f"Customer type: {row['customer_type']}. "
                            f"Room type: {row['reserved_room_type']}. "
                            f"Lead time: {row['lead_time']} days."), 
                axis=1
            )
            
            # Initialize the FAISS-based vector store using the 'summary' column
            self.vector_store = VectorStore(self.df, text_column='summary')
            
            # Initialize the SentenceTransformer for predefined question matching
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.questions = [
                "Show me total revenue for July 2017",
                "Which locations had the highest booking cancellations?",
                "What is the average price of a hotel booking?",
                "What is the most common length of stay?",
                "Which month has the highest number of bookings?",
                "What percentage of bookings are cancelled?",
                "What is the average daily rate for each room type?",
                "Which market segment generates the most revenue?",
                "What is the distribution of customer types?",
                "How many bookings include children or babies?"
            ]
            self.embeddings = self.model.encode(self.questions)
            
            # Keep a performance metrics log
            self.metrics = {
                "query_times": [],
                "avg_response_time": 0,
                "successful_queries": 0,
                "failed_queries": 0
            }
            
            logger.info("HotelAnalytics initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing HotelAnalytics: {str(e)}")
            raise
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generates a comprehensive analytics report from the hotel booking data.
        
        Returns:
            Dict[str, Any]: A dictionary containing various analytics metrics
        """
        try:
            # Total bookings and average daily rate
            total_bookings = len(self.df)
            average_daily_rate = self.df['adr'].mean()
            
            # Cancellation rate (assuming 'is_canceled' exists as 0 or 1)
            cancellation_rate = (self.df['is_canceled'].mean() * 100) if 'is_canceled' in self.df.columns else None
            
            # Revenue trends over time: group by arrival year and month, summing total_price
            if 'arrival_date_year' in self.df.columns and 'arrival_date_month' in self.df.columns:
                revenue_trends = (
                    self.df.groupby(['arrival_date_year', 'arrival_date_month'])['total_price']
                    .sum()
                    .reset_index()
                    .to_dict(orient='records')
                )
            else:
                revenue_trends = "Arrival date information not available."
            
            # Geographical distribution: count bookings by country
            geographical_distribution = self.df['country'].value_counts().to_dict() if 'country' in self.df.columns else {}
            
            # Booking lead time statistics (assuming 'lead_time' exists)
            if 'lead_time' in self.df.columns:
                lead_time_stats = {
                    "min": int(self.df['lead_time'].min()),
                    "max": int(self.df['lead_time'].max()),
                    "mean": round(self.df['lead_time'].mean(), 2),
                    "median": int(self.df['lead_time'].median())
                }
            else:
                lead_time_stats = "Lead time information not available."
            
            # Other analytics
            most_common_customer_type = self.df['customer_type'].mode()[0] if 'customer_type' in self.df.columns else "N/A"
            most_booked_room_type = self.df['reserved_room_type'].mode()[0] if 'reserved_room_type' in self.df.columns else "N/A"
            if 'stays_in_weekend_nights' in self.df.columns and 'stays_in_week_nights' in self.df.columns:
                average_length_of_stay = (self.df['stays_in_weekend_nights'] + self.df['stays_in_week_nights']).mean()
            else:
                average_length_of_stay = "N/A"
            
            report = {
                "total_bookings": total_bookings,
                "average_daily_rate": round(average_daily_rate, 2),
                "cancellation_rate (%)": round(cancellation_rate, 2) if cancellation_rate is not None else "N/A",
                "revenue_trends": revenue_trends,
                "geographical_distribution": geographical_distribution,
                "lead_time_stats": lead_time_stats,
                "most_common_customer_type": most_common_customer_type,
                "most_booked_room_type": most_booked_room_type,
                "average_length_of_stay": round(average_length_of_stay, 2) if average_length_of_stay != "N/A" else "N/A"
            }
            return report
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {"error": str(e)}
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answers a natural language question about the hotel booking data using 
        the LLM-powered RAG system.
        
        Parameters:
            question (str): The question to answer
            
        Returns:
            Dict[str, Any]: A dictionary containing the answer and other metadata
        """
        start_time = time.time()
        
        try:
            # First, extract specific metrics or structured data that might help answer the question
            metadata = self._extract_relevant_metrics(question)
            
            # Use the LLM-powered RAG to generate an answer
            result = self.vector_store.generate_answer(question, metadata)
            
            # Track performance metrics
            query_time = time.time() - start_time
            self.metrics["query_times"].append(query_time)
            self.metrics["avg_response_time"] = sum(self.metrics["query_times"]) / len(self.metrics["query_times"])
            self.metrics["successful_queries"] += 1
            
            # Add performance data to result
            result["query_time_seconds"] = round(query_time, 3)
            
            return result
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            self.metrics["failed_queries"] += 1
            
            # Fallback to the original method for robustness
            try:
                result = self._legacy_answer_question(question)
                return result
            except:
                return {"answer": f"I encountered an error while processing your question: {str(e)}"}
    
    def _extract_relevant_metrics(self, question: str) -> Dict[str, Any]:
        """
        Extracts metrics from the data that are relevant to the question.
        This provides additional structured context for the LLM.
        
        Parameters:
            question (str): The question being asked
            
        Returns:
            Dict[str, Any]: A dictionary of relevant metrics
        """
        metrics = {}
        
        # Check for keywords in the question and extract relevant metrics
        question_lower = question.lower()
        
        # Revenue related
        if any(term in question_lower for term in ["revenue", "income", "earnings", "money"]):
            metrics["total_revenue"] = round(self.df["total_price"].sum(), 2)
            
        # Time period related
        for month in ["january", "february", "march", "april", "may", "june", 
                    "july", "august", "september", "october", "november", "december"]:
            if month in question_lower:
                metrics[f"{month}_bookings"] = len(self.df[self.df["arrival_date_month"].str.lower() == month.capitalize()])
                
        for year in ["2015", "2016", "2017", "2018", "2019"]:
            if year in question_lower:
                metrics[f"year_{year}_bookings"] = len(self.df[self.df["arrival_date_year"] == int(year)])
                
        # Country related
        for country in self.df["country"].unique():
            country_lower = str(country).lower()
            if country_lower in question_lower:
                country_data = self.df[self.df["country"] == country]
                metrics[f"{country}_bookings"] = len(country_data)
                metrics[f"{country}_revenue"] = round(country_data["total_price"].sum(), 2)
                metrics[f"{country}_cancellation_rate"] = round(country_data["is_canceled"].mean() * 100, 2)
                
        # Add some general metrics if the question is generic
        if len(metrics) < 2:
            metrics["total_bookings"] = len(self.df)
            metrics["average_daily_rate"] = round(self.df["adr"].mean(), 2)
            metrics["cancellation_rate"] = round(self.df["is_canceled"].mean() * 100, 2)
            
        return metrics
    
    def _legacy_answer_question(self, question: str) -> Dict[str, Any]:
        """
        Legacy method for answering questions as a fallback
        """
        # Use the FAISS vector store to retrieve relevant context from booking summaries.
        retrieved = self.vector_store.query(question, top_k=3)
        context = " ".join([item['text'] for item in retrieved])
        
        # Also, perform predefined question matching using cosine similarity.
        question_embedding = self.model.encode([question])
        similarities = cosine_similarity(question_embedding, self.embeddings)[0]
        most_similar_idx = np.argmax(similarities)
        
        # If similarity is too low, fallback to returning the FAISS context.
        if similarities[most_similar_idx] < 0.5:
            return {"answer": f"Based on our data: {context}"}
        
        # Based on the most similar predefined question, compute a detailed answer:
        if most_similar_idx == 0:
            # "Show me total revenue for July 2017"
            if 'arrival_date_year' in self.df.columns and 'arrival_date_month' in self.df.columns:
                july_2017 = self.df[(self.df['arrival_date_month'] == 'July') & (self.df['arrival_date_year'] == 2017)]
                revenue = july_2017['total_price'].sum()
                return {"answer": f"The total revenue for July 2017 was ${revenue:,.2f}"}
            else:
                return {"answer": f"Date information not available."}
        elif most_similar_idx == 1:
            # "Which locations had the highest booking cancellations?"
            if 'is_canceled' in self.df.columns and 'country' in self.df.columns:
                cancellations = self.df[self.df['is_canceled'] == 1]['country'].value_counts().head(5)
                return {"answer": f"Top 5 countries with highest cancellations: {dict(cancellations)}"}
            else:
                return {"answer": f"Cancellation or country data not available."}
        
        # Implement other question types as in the original code...
        # ...
        
        return {"answer": f"I don't have enough information to answer that specifically."}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Returns performance metrics about the Q&A system
        """
        return {
            "avg_response_time_seconds": round(self.metrics["avg_response_time"], 3),
            "successful_queries": self.metrics["successful_queries"],
            "failed_queries": self.metrics["failed_queries"],
            "total_queries": self.metrics["successful_queries"] + self.metrics["failed_queries"]
        }
