"""
Core RAG functionality for the Teaching Assistant
Supports OpenAI (default) and Anthropic for inference
"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import os
from typing import Tuple
import openai
from anthropic import Anthropic


class RAGAssistant:
    """RAG Assistant for querying course content"""
    
    def __init__(self, embeddings_path: str = 'embeddings.joblib'):
        """
        Initialize RAG Assistant
        
        Args:
            embeddings_path: Path to the joblib file containing embeddings
        """
        self.df = joblib.load(embeddings_path)

        # Only OpenAI embeddings and model
        self.llm_provider = "openai"
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        self.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

        # OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY", None)
        if openai_api_key:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        else:
            self.openai_client = None

        # Anthropic (optional)
        self.anthropic_client = None
    
    
    def set_openai_config(self, api_key: str, embedding_model: str, llm_model: str):
        """Configure OpenAI manually if needed"""
        self.llm_provider = "openai"
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.openai_client = openai.OpenAI(api_key=api_key)
    
    
    def create_embedding(self, text_list: list) -> list:
        """Always create embeddings using OpenAI"""
        return self._create_openai_embedding(text_list)
    
    
    def _create_openai_embedding(self, text_list: list) -> list:
        """Create embeddings using OpenAI"""
        if not self.openai_client:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        embeddings = []
        for text in text_list:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    
    def inference(self, prompt: str) -> str:
        """Always use OpenAI for inference"""
        return self._openai_inference(prompt)
    
    
    def _openai_inference(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        if not self.openai_client:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        response = self.openai_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a helpful teaching assistant that guides students to relevant course content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    
    def query(self, incoming_query: str, top_k: int = 5) -> Tuple[str, pd.DataFrame]:
        """
        Query the RAG system
        
        Args:
            incoming_query: User's question
            top_k: Number of top results to retrieve
            
        Returns:
            Tuple of (response_text, relevant_chunks_dataframe)
        """
        # Create embedding for the query
        question_embedding = self.create_embedding([incoming_query])[0]
        
        # Find similarities
        similarities = cosine_similarity(
            np.vstack(self.df['embedding'].values),
            [question_embedding]
        ).flatten()
        
        # Get top results
        max_indx = similarities.argsort()[::-1][0:top_k]
        new_df = self.df.loc[max_indx].copy()
        
        # Create prompt
        prompt = f'''I am teaching web development in my Sigma WDT course. Here are subtitle chunks containing:
video title, video number, start time, end time, text:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
User asked: "{incoming_query}"

Answer in a human-friendly tone, clearly explaining:
- which video has relevant content
- timestamps to view
- what that content teaches

If the user's question is unrelated to this course, politely tell them that you can only answer questions related to the video content.
'''
        
        # Generate response
        response = self.inference(prompt)
        
        return response, new_df


