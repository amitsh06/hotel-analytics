"""
LLM-powered reasoning module for the Hotel Analytics system.
Uses a lightweight open-source LLM model to provide context-aware answers.
"""

import os
import torch
from typing import List, Dict, Any, Optional, Tuple
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMReasoner:
    """
    LLM-based reasoning component that enhances the RAG pipeline with generative capabilities.
    Uses a lightweight open-source model (Phi-2) for inference.
    """
    
    def __init__(self, model_name: str = "microsoft/phi-2", device: str = None):
        """
        Initialize the LLM reasoner with the specified model.
        
        Args:
            model_name: The Hugging Face model identifier
            device: Device to run on ('cpu', 'cuda', 'mps'). If None, automatically detect.
        """
        self.model_name = model_name
        
        # Automatically detect the best available device if not specified
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            if self.device == "cpu" and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.device = "mps"  # For Apple Silicon
        else:
            self.device = device
            
        logger.info(f"Initializing LLM Reasoner with model {model_name} on {self.device}")
        
        try:
            # Load the model with 8-bit quantization for efficiency
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Use lower precision for efficiency
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device != "cpu" else torch.float32,
                device_map=self.device,
                low_cpu_mem_usage=True
            )
            
            # Create a text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            logger.info("LLM Reasoner initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            raise
    
    def generate_answer(self, question: str, context: List[str], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate an answer based on the question, retrieved context, and metadata.
        
        Args:
            question: The user question
            context: Retrieved passages or documents from the vector store
            metadata: Additional structured data or metrics related to the question
        
        Returns:
            A natural language answer to the question
        """
        # Format metadata if available
        metadata_text = ""
        if metadata:
            metadata_text = "Additional data:\n"
            for key, value in metadata.items():
                metadata_text += f"- {key}: {value}\n"
        
        # Combine context passages
        context_text = "\n".join([f"- {c}" for c in context])
        
        # Create a prompt for the model
        prompt = f"""You are a hotel analytics assistant that provides accurate information about hotel bookings and data.
Answer the following question based on the provided context and additional data.

Question: {question}

Context:
{context_text}

{metadata_text}

Based on the above information, the answer is:"""
        
        try:
            # Generate the response
            outputs = self.generator(prompt, max_new_tokens=150, num_return_sequences=1)
            
            # Extract the generated text
            generated_text = outputs[0]['generated_text']
            
            # Extract just the answer part (after the prompt)
            answer = generated_text[len(prompt):].strip()
            
            # If the answer is empty, return a fallback response
            if not answer:
                return "I don't have enough information to answer that question accurately."
                
            return answer
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return f"I encountered an error while processing your question. Please try again."
    
    def __call__(self, question: str, context: List[str], metadata: Optional[Dict[str, Any]] = None) -> str:
        """Convenience method to allow the class to be called directly."""
        return self.generate_answer(question, context, metadata) 