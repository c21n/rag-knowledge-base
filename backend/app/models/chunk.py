"""
Chunk models for text segments and embeddings.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class ChunkBase(BaseModel):
    """Base chunk model with core fields."""
    content: str = Field(..., min_length=1, description="Chunk text content")
    document_id: str = Field(..., description="Parent document ID")
    chunk_index: int = Field(..., ge=0, description="Position in document")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "This is a sample chunk of text.",
                "document_id": "doc-123",
                "chunk_index": 0,
                "metadata": {"page": 1, "section": "intro"}
            }
        }


class Chunk(ChunkBase):
    """Complete chunk model with ID and timestamps."""
    id: str = Field(..., description="Unique chunk identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "chunk-456",
                "content": "This is a sample chunk of text.",
                "document_id": "doc-123",
                "chunk_index": 0,
                "metadata": {"page": 1},
                "created_at": "2024-01-01T00:00:00"
            }
        }


class ChunkWithEmbedding(Chunk):
    """Chunk with embedding vector for storage and retrieval."""
    embedding: List[float] = Field(..., description="Vector embedding")
    
    @validator('embedding')
    def validate_embedding(cls, v):
        """Ensure embedding is a list of floats."""
        if not isinstance(v, list):
            raise ValueError("Embedding must be a list")
        if len(v) == 0:
            raise ValueError("Embedding cannot be empty")
        # Validate first element is float-like
        try:
            float(v[0])
        except (ValueError, TypeError):
            raise ValueError("Embedding must be a list of floats")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "chunk-456",
                "content": "This is a sample chunk.",
                "document_id": "doc-123",
                "chunk_index": 0,
                "metadata": {},
                "created_at": "2024-01-01T00:00:00",
                "embedding": [0.1, 0.2, 0.3, 0.4]
            }
        }


class SearchResult(BaseModel):
    """Search result with chunk and similarity score."""
    chunk: Chunk = Field(..., description="Matching chunk")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "chunk": {
                    "id": "chunk-456",
                    "content": "Relevant text here.",
                    "document_id": "doc-123",
                    "chunk_index": 2,
                    "metadata": {},
                    "created_at": "2024-01-01T00:00:00"
                },
                "score": 0.89
            }
        }


class SearchRequest(BaseModel):
    """Search request body."""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "machine learning applications",
                "top_k": 5
            }
        }


class SearchResponse(BaseModel):
    """Search response with results and metadata."""
    query: str = Field(..., description="Original query")
    results: List[SearchResult] = Field(default=[], description="Search results")
    total_results: int = Field(..., ge=0, description="Total number of results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "machine learning",
                "results": [
                    {
                        "chunk": {
                            "id": "chunk-1",
                            "content": "ML is...",
                            "document_id": "doc-123",
                            "chunk_index": 0,
                            "created_at": "2024-01-01T00:00:00"
                        },
                        "score": 0.92
                    }
                ],
                "total_results": 1
            }
        }
