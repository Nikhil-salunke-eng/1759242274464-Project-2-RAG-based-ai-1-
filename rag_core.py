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
        self.llm_provider = "ollama"
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "bge-m3")
        self.llm_model = os.getenv("LLM_MODEL", "llama3.2")
        self.openai_client = None
        self.anthropic_client = None
        
    def set_ollama_config(self, url: str, embedding_model: str, llm_model: str):
        """Configure Ollama settings"""
        self.llm_provider = "ollama"
        self.ollama_url = url
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        
    def set_openai_config(self, api_key: str, embedding_model: str, llm_model: str):
        """Configure OpenAI settings"""
        self.llm_provider = "openai"
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.openai_client = openai.OpenAI(api_key=api_key)
        
    def set_anthropic_config(self, api_key: str, embedding_model: str, llm_model: str):
        """Configure Anthropic settings"""
        self.llm_provider = "anthropic"
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.anthropic_client = Anthropic(api_key=api_key)
    
    def create_embedding(self, text_list: list) -> list:
        """
        Create embeddings for text list
        
        Args:
            text_list: List of texts to embed
            
        Returns:
            List of embeddings
        """
        if self.llm_provider == "ollama":
            return self._create_ollama_embedding(text_list)
        elif self.llm_provider == "openai":
            return self._create_openai_embedding(text_list)
        else:
            # For Anthropic, we'll use OpenAI embeddings (Anthropic doesn't have embedding API)
            if not self.openai_client:
                raise ValueError("OpenAI client not initialized. Anthropic requires OpenAI for embeddings.")
            return self._create_openai_embedding(text_list)
    
    def _create_ollama_embedding(self, text_list: list) -> list:
        """Create embeddings using Ollama"""
        r = requests.post(
            f"{self.ollama_url}/api/embed",
            json={
                "model": self.embedding_model,
                "input": text_list
            },
            timeout=60
        )
        r.raise_for_status()
        return r.json()["embeddings"]
    
    def _create_openai_embedding(self, text_list: list) -> list:
        """Create embeddings using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        embeddings = []
        for text in text_list:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    def inference(self, prompt: str) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated response text
        """
        if self.llm_provider == "ollama":
            return self._ollama_inference(prompt)
        elif self.llm_provider == "openai":
            return self._openai_inference(prompt)
        else:  # anthropic
            return self._anthropic_inference(prompt)
    
    def _ollama_inference(self, prompt: str) -> str:
        """Generate response using Ollama"""
        r = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.llm_model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        r.raise_for_status()
        return r.json()["response"]
    
    def _openai_inference(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        response = self.openai_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a helpful teaching assistant that guides students to relevant course content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def _anthropic_inference(self, prompt: str) -> str:
        """Generate response using Anthropic"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")
        
        message = self.anthropic_client.messages.create(
            model=self.llm_model,
            max_tokens=1024,
            system="You are a helpful teaching assistant that guides students to relevant course content.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    
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

