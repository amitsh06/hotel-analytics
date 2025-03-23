import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, data: pd.DataFrame, text_column: str, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the vector store with data embeddings.

        Parameters:
        - data (pd.DataFrame): The DataFrame containing the data to index.
        - text_column (str): The column name in the DataFrame containing text to embed.
        - model_name (str): The SentenceTransformer model to use for embedding generation.
        """
        # Initialize the SentenceTransformer model
        self.model = SentenceTransformer(model_name)
        
        # Store the DataFrame and extract the texts from the specified column
        self.data = data
        self.texts = data[text_column].tolist()
        
        # Generate embeddings for all texts and convert them to float32 (required by FAISS)
        self.embeddings = self.model.encode(self.texts)
        self.embeddings = np.array(self.embeddings).astype("float32")
        
        # Determine the dimension of the embeddings
        self.dimension = self.embeddings.shape[1]
        
        # Create a FAISS index (using L2 distance)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings)
        
        # Initialize LLM reasoner to None (will be loaded on demand to save resources)
        self.llm_reasoner = None
    
    def query(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Queries the FAISS index with the given query text and returns the top_k similar texts.

        Parameters:
        - query_text (str): The query string to search for.
        - top_k (int): The number of top similar results to return.

        Returns:
        - List[Dict]: A list of dictionaries, each containing the retrieved text and its distance.
        """
        # Generate the embedding for the query text
        query_embedding = self.model.encode([query_text])
        query_embedding = np.array(query_embedding).astype("float32")
        
        # Search the FAISS index for the top_k nearest neighbors
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Prepare the results list with text and distance
        results = [
            {"text": self.texts[idx], "distance": float(dist), "index": int(idx)}
            for idx, dist in zip(indices[0], distances[0])
        ]
        return results
    
    def _load_llm_reasoner(self):
        """
        Lazily loads the LLM reasoner when needed.
        """
        if self.llm_reasoner is None:
            try:
                # Import here to avoid circular imports
                from src.analytics.llm import LLMReasoner
                self.llm_reasoner = LLMReasoner()
                logger.info("LLM reasoner loaded successfully")
            except Exception as e:
                logger.error(f"Error loading LLM reasoner: {str(e)}")
                # Create a dummy reasoner that returns a fallback message
                self.llm_reasoner = lambda question, context, metadata: (
                    "I'm unable to process this question with the LLM component. "
                    "Here's the retrieved information instead: " + "; ".join(context)
                )
    
    def generate_answer(self, query_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generates an answer to the query using RAG (Retrieval-Augmented Generation).
        
        Parameters:
        - query_text (str): The query string to answer.
        - metadata (Dict): Additional structured data relevant to the query.
        
        Returns:
        - Dict: A dictionary with the answer and confidence score.
        """
        # Retrieve relevant contexts
        retrieval_results = self.query(query_text, top_k=5)
        retrieved_texts = [result["text"] for result in retrieval_results]
        
        # Calculate a simple confidence score based on retrieval distances
        confidence = 0.0
        if retrieval_results:
            # Convert distances to similarity scores (smaller distance = higher similarity)
            max_distance = max(result["distance"] for result in retrieval_results)
            similarities = [1.0 - (result["distance"] / (max_distance + 1e-5)) for result in retrieval_results]
            confidence = sum(similarities) / len(similarities)
        
        # Load the LLM reasoner if not already loaded
        self._load_llm_reasoner()
        
        # Get indices of retrieved documents to fetch additional metadata
        doc_indices = [result["index"] for result in retrieval_results]
        
        # Extract relevant rows from the original DataFrame
        relevant_data = self.data.iloc[doc_indices].to_dict('records') if doc_indices else []
        
        # Add relevant_data to metadata if provided
        if metadata is None:
            metadata = {}
        metadata["relevant_records"] = relevant_data[:2]  # Limit to first 2 records to avoid overloading
        
        # Generate answer using LLM
        answer = self.llm_reasoner(query_text, retrieved_texts, metadata)
        
        return {
            "answer": answer,
            "confidence": float(confidence),
            "retrieved_contexts": retrieved_texts[:3]  # Return top 3 contexts for reference
        }
