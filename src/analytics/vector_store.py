import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd

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
    
    def query(self, query_text: str, top_k: int = 3):
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
            {"text": self.texts[idx], "distance": float(dist)}
            for idx, dist in zip(indices[0], distances[0])
        ]
        return results
