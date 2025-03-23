import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.analytics.vector_store import VectorStore


class HotelAnalytics:
    def __init__(self):
        # Load the processed CSV file
        file_path = r"C:\Users\maith\OneDrive - Manipal University Jaipur\Desktop\hotel analytics\src\data\processed\hotel_bookings_processed.csv"
        self.df = pd.read_csv(file_path)
        
        # Create a summary column to be indexed by the vector store.
        # You can customize this summary as needed.
        self.df['summary'] = self.df.apply(
            lambda row: f"Booking from {row['country']} with ADR ${row['adr']} and total nights {row['total_nights']}.", 
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
    
    def generate_report(self):
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
    
    def answer_question(self, question: str):
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
                return {"answer": f"The total revenue for July 2017 was ${revenue:,.2f}. Context: {context}"}
            else:
                return {"answer": f"Date information not available. Context: {context}"}
        elif most_similar_idx == 1:
            # "Which locations had the highest booking cancellations?"
            if 'is_canceled' in self.df.columns and 'country' in self.df.columns:
                cancellations = self.df[self.df['is_canceled'] == 1]['country'].value_counts().head(5)
                return {"answer": f"Top 5 countries with highest cancellations: {dict(cancellations)}. Context: {context}"}
            else:
                return {"answer": f"Cancellation or country data not available. Context: {context}"}
        elif most_similar_idx == 2:
            # "What is the average price of a hotel booking?"
            avg_price = self.df['adr'].mean()
            return {"answer": f"The average price per night is ${avg_price:.2f}. Context: {context}"}
        elif most_similar_idx == 3:
            # "What is the most common length of stay?"
            total_nights = self.df['stays_in_weekend_nights'] + self.df['stays_in_week_nights']
            most_common = total_nights.mode()[0]
            return {"answer": f"The most common length of stay is {most_common} nights. Context: {context}"}
        elif most_similar_idx == 4:
            # "Which month has the highest number of bookings?"
            if 'arrival_date_month' in self.df.columns:
                busiest_month = self.df['arrival_date_month'].mode()[0]
                return {"answer": f"The month with the highest number of bookings is {busiest_month}. Context: {context}"}
            else:
                return {"answer": f"Month data not available. Context: {context}"}
        elif most_similar_idx == 5:
            # "What percentage of bookings are cancelled?"
            cancel_rate = self.df['is_canceled'].mean() * 100
            return {"answer": f"{cancel_rate:.1f}% of bookings are cancelled. Context: {context}"}
        elif most_similar_idx == 6:
            # "What is the average daily rate for each room type?"
            if 'reserved_room_type' in self.df.columns:
                avg_by_room = self.df.groupby('reserved_room_type')['adr'].mean()
                return {"answer": f"Average daily rates by room type: {dict(avg_by_room.round(2))}. Context: {context}"}
            else:
                return {"answer": f"Room type data not available. Context: {context}"}
        elif most_similar_idx == 7:
            # "Which market segment generates the most revenue?"
            if 'market_segment' in self.df.columns:
                segment_revenue = self.df.groupby('market_segment').apply(
                    lambda x: x['total_price'].sum()
                ).sort_values(ascending=False)
                return {"answer": f"Revenue by market segment: {dict(segment_revenue.round(2))}. Context: {context}"}
            else:
                return {"answer": f"Market segment data not available. Context: {context}"}
        elif most_similar_idx == 8:
            # "What is the distribution of customer types?"
            if 'customer_type' in self.df.columns:
                customer_dist = (self.df['customer_type'].value_counts() / len(self.df) * 100).round(1)
                return {"answer": f"Customer type distribution: {dict(customer_dist)}%. Context: {context}"}
            else:
                return {"answer": f"Customer type data not available. Context: {context}"}
        elif most_similar_idx == 9:
            # "How many bookings include children or babies?"
            if 'children' in self.df.columns and 'babies' in self.df.columns:
                with_kids = len(self.df[(self.df['children'] > 0) | (self.df['babies'] > 0)])
                percentage = with_kids / len(self.df) * 100
                return {"answer": f"{percentage:.1f}% of bookings ({with_kids} bookings) include children or babies. Context: {context}"}
            else:
                return {"answer": f"Children or babies data not available. Context: {context}"}
        
        return {"answer": f"This is a placeholder answer. Context: {context}"}
