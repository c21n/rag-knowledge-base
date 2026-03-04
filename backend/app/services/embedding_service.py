"""
Embedding service for generating vector embeddings using OpenAI-compatible API.
Supports Alibaba Bailian via OpenAI-compatible mode.
"""
import os
import logging
from typing import List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the embedding service.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            base_url: API base URL (defaults to OPENAI_BASE_URL env var or OpenAI default)
        """
        from src.config import get_settings
        settings = get_settings()
        
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.base_url = base_url or settings.OPENAI_BASE_URL
        self.model = settings.OPENAI_EMBEDDING_MODEL
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set. Embeddings will fail.")
        
        # Import here to avoid dependency issues during initialization
        try:
            from langchain_openai import OpenAIEmbeddings
            
            # Configure embeddings with custom base_url for Alibaba Bailian
            embeddings_kwargs = {
                "model": self.model,
                "api_key": self.api_key,
            }
            
            # Add base_url if provided (for Alibaba Bailian compatibility)
            if self.base_url:
                embeddings_kwargs["base_url"] = self.base_url
                logger.info(f"Using custom base URL: {self.base_url}")
            
            self._embeddings = OpenAIEmbeddings(**embeddings_kwargs)
            logger.info(f"EmbeddingService initialized with model: {self.model}")
            
        except ImportError as e:
            logger.error(f"Failed to import langchain_openai: {e}")
            self._embeddings = None
    
    def get_embedding_model(self) -> str:
        """Return the embedding model name."""
        return self.model
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
            
        Raises:
            RuntimeError: If embedding generation fails
        """
        if not self._embeddings:
            raise RuntimeError("Embedding service not properly initialized")
        
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not configured")
        
        try:
            start_time = datetime.utcnow()
            logger.info(f"Generating embedding for text ({len(text)} chars)")
            
            embedding = self._embeddings.embed_query(text)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Embedding generated in {duration:.2f}s, dimensions: {len(embedding)}")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise RuntimeError(f"Embedding generation failed: {e}")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch processing).
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            RuntimeError: If embedding generation fails
        """
        if not self._embeddings:
            raise RuntimeError("Embedding service not properly initialized")
        
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not configured")
        
        if not texts:
            return []
        
        try:
            start_time = datetime.utcnow()
            total_chars = sum(len(t) for t in texts)
            logger.info(f"Generating embeddings for {len(texts)} texts ({total_chars} total chars)")
            
            embeddings = self._embeddings.embed_documents(texts)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Batch embeddings generated in {duration:.2f}s, count: {len(embeddings)}")
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise RuntimeError(f"Batch embedding generation failed: {e}")
    
    def get_token_count(self, text: str) -> int:
        """
        Estimate token count for text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Estimated token count
        """
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
            return len(encoding.encode(text))
        except:
            # Fallback: rough estimate (4 chars per token)
            return len(text) // 4


# Singleton instance for application-wide use
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get or create the embedding service singleton."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


def reset_embedding_service():
    """Reset the singleton instance (useful for testing)."""
    global _embedding_service
    _embedding_service = None
