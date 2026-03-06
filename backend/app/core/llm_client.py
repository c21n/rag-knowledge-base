"""
LLM client for generating text using Alibaba Bailian API (OpenAI-compatible mode).
Supports both streaming and non-streaming generation.
"""
import os
import logging
from typing import Optional, Generator
from datetime import datetime

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for LLM text generation using OpenAI-compatible API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize the LLM client.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            base_url: API base URL (defaults to OPENAI_BASE_URL env var)
            model: Model name (defaults to qwen-turbo)
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
        """
        from src.config import get_settings
        settings = get_settings()
        
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.base_url = base_url or settings.OPENAI_BASE_URL
        self.model = model or os.getenv("LLM_MODEL", "qwen-turbo")
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set. LLM generation will fail.")
        
        # Import here to avoid dependency issues during initialization
        try:
            from langchain_openai import ChatOpenAI
            
            # Configure chat model with custom base_url for Alibaba Bailian
            chat_kwargs = {
                "model": self.model,
                "api_key": self.api_key,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
            
            # Add base_url if provided (for Alibaba Bailian compatibility)
            if self.base_url:
                chat_kwargs["base_url"] = self.base_url
                logger.info(f"Using custom base URL: {self.base_url}")
            
            self._chat = ChatOpenAI(**chat_kwargs)
            logger.info(f"LLMClient initialized with model: {self.model}")
            
        except ImportError as e:
            logger.error(f"Failed to import langchain_openai: {e}")
            self._chat = None
    
    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate text response using LLM.
        
        Args:
            prompt: User question or prompt
            context: Optional context for RAG (retrieved documents)
            
        Returns:
            Generated text response
            
        Raises:
            RuntimeError: If generation fails
        """
        if not self._chat:
            raise RuntimeError("LLM client not properly initialized")
        
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not configured")
        
        try:
            start_time = datetime.utcnow()
            logger.info(f"Generating response for prompt ({len(prompt)} chars)")
            
            # Build messages
            messages = []
            
            # Add context if provided
            if context:
                messages.append({
                    "role": "system",
                    "content": f"参考文档:\n{context}"
                })
            
            # Add user prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Generate response
            from langchain_core.messages import HumanMessage, SystemMessage
            langchain_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    langchain_messages.append(SystemMessage(content=msg["content"]))
                else:
                    langchain_messages.append(HumanMessage(content=msg["content"]))
            
            response = self._chat.invoke(langchain_messages)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Response generated in {duration:.2f}s")
            
            return response.content
            
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise RuntimeError(f"LLM generation failed: {e}")
    
    def generate_stream(self, prompt: str, context: Optional[str] = None) -> Generator[str, None, None]:
        """
        Generate streaming text response using LLM.
        
        Args:
            prompt: User question or prompt
            context: Optional context for RAG (retrieved documents)
            
        Yields:
            Text chunks as they are generated
            
        Raises:
            RuntimeError: If generation fails
        """
        if not self._chat:
            raise RuntimeError("LLM client not properly initialized")
        
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not configured")
        
        try:
            logger.info(f"Starting streaming generation for prompt ({len(prompt)} chars)")
            
            # Build messages
            messages = []
            
            # Add context if provided
            if context:
                messages.append({
                    "role": "system",
                    "content": f"参考文档:\n{context}"
                })
            
            # Add user prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Generate streaming response
            from langchain_core.messages import HumanMessage, SystemMessage
            langchain_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    langchain_messages.append(SystemMessage(content=msg["content"]))
                else:
                    langchain_messages.append(HumanMessage(content=msg["content"]))
            
            for chunk in self._chat.stream(langchain_messages):
                if chunk.content:
                    yield chunk.content
            
            logger.info("Streaming generation completed")
            
        except Exception as e:
            logger.error(f"Failed to generate streaming response: {e}")
            raise RuntimeError(f"LLM streaming generation failed: {e}")
    
    def get_model_name(self) -> str:
        """Return the model name."""
        return self.model


# Singleton instance for application-wide use
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the LLM client singleton."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def reset_llm_client():
    """Reset the singleton instance (useful for testing)."""
    global _llm_client
    _llm_client = None