"""
Core RAG functionality for the Teaching Assistant
Supports multiple LLM providers: Ollama, OpenAI, Anthropic
"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests
import os
from typing import Tuple, Optional
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

        # DEFAULT PROVIDER = OPENAI
        self.llm_provider = "openai"

        # DEFAULT MODELS (OpenAI)
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        self.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

        # OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY", None)
        if openai_api_key:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        else:
            self.openai_client = None

        # Ollama config (optional local)
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")

        # Anthropic (optional)
        self.anthropic_client = None
    
    
    def set_openai_config(self, api_key: str, embedding_model: str, llm_model: str):
        """Configure OpenAI settings"""
        self.llm_provider = "openai"
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.openai_client = openai.OpenAI(api_key=api_key)
    
    
    def create_embedding(self, text_list: list) -> list:
        """
        Create embeddings for text list
        
        Args:
            text_list: List of texts to embed
            
        Returns:
            List of embeddings
        """
        return self._create_openai_embedding(text_list)
    
    
    def _create_openai_embedding(self, text_list: list) -> list:
        """Create embeddings using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI API Key not found. Set OPENAI_API_KEY env variable.")
        
        embeddings = []
        for text in text_list:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    
    def inference(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        return self._openai_inference(prompt)
    
    
    def _openai_inference(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI API Key not found. Set OPENAI_API_KEY env variable.")
        
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
        prompt = f'''I am teaching web development in my Sigma web development course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course
'''
        
        # Generate response
        response = self.inference(prompt)
        
        return response, new_df

