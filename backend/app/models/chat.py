"""
Chat request and response models for RAG-based Q&A.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SourceCitation(BaseModel):
    """Citation for a source document in the response."""
    
    document_id: str = Field(..., description="Document ID")
    chunk_index: int = Field(..., ge=0, description="Chunk index in the document")
    content_preview: str = Field(..., min_length=1, description="Preview of chunk content")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc-123",
                "chunk_index": 5,
                "content_preview": "Machine learning is a subset of artificial intelligence...",
                "score": 0.92
            }
        }


class ChatRequest(BaseModel):
    """Request model for RAG chat endpoint."""
    
    query: str = Field(..., min_length=1, max_length=2000, description="User question or query")
    role_id: Optional[str] = Field(None, description="Optional role/agent ID for context")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation continuity")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of documents to retrieve")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "什么是机器学习？",
                "role_id": "default",
                "session_id": "session-abc123",
                "top_k": 5
            }
        }


class ChatResponse(BaseModel):
    """Response model for RAG chat endpoint."""
    
    answer: str = Field(..., description="Generated answer from LLM")
    sources: List[SourceCitation] = Field(default=[], description="Source document citations")
    response_time: float = Field(..., ge=0.0, description="Response time in seconds")
    retrieved_count: int = Field(default=0, ge=0, description="Number of documents retrieved")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "机器学习是人工智能的一个分支，它使计算机能够从数据中学习并做出决策 [source: doc-123]。机器学习算法通过训练数据来识别模式并进行预测 [source: doc-456]。",
                "sources": [
                    {
                        "document_id": "doc-123",
                        "chunk_index": 5,
                        "content_preview": "Machine learning is a subset of artificial intelligence...",
                        "score": 0.92
                    },
                    {
                        "document_id": "doc-456",
                        "chunk_index": 12,
                        "content_preview": "ML algorithms identify patterns in training data...",
                        "score": 0.88
                    }
                ],
                "response_time": 1.23,
                "retrieved_count": 5
            }
        }


class ChatHistory(BaseModel):
    """Chat history for a session."""
    
    session_id: str = Field(..., description="Session identifier")
    messages: List[dict] = Field(default=[], description="List of chat messages")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session-abc123",
                "messages": [
                    {"role": "user", "content": "什么是机器学习？"},
                    {"role": "assistant", "content": "机器学习是人工智能的一个分支..."}
                ],
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:05:00"
            }
        }