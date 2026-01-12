"""
LLM Service - OpenAI Integration
"""
from typing import List, Dict, Optional
import openai
from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class LLMService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        openai.api_base = settings.OPENAI_API_BASE
        self.model = settings.OPENAI_MODEL
        
    async def generate_response(
        self,
        query: str,
        context: str = "",
        history: List[Dict] = None
    ) -> str:
        """
        Generate response using OpenAI
        """
        try:
            messages = self._build_messages(query, context, history)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            logger.info("Successfully generated response")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def _build_messages(
        self,
        query: str,
        context: str,
        history: List[Dict]
    ) -> List[Dict]:
        """Build message array for OpenAI"""
        messages = [
            {
                "role": "system",
                "content": """You are a helpful AI assistant. 
                Answer questions based on provided context when available.
                Be concise and accurate."""
            }
        ]
        
        # Add history
        if history:
            for item in history[-3:]:  # Last 3 interactions
                messages.append({"role": "user", "content": item["query"]})
                messages.append({"role": "assistant", "content": item["answer"]})
        
        # Add context if available
        if context:
            messages.append({
                "role": "system",
                "content": f"Context from documents:\n{context}"
            })
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        return messages