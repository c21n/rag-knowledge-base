"""Pydantic models for document operations in the RAG Knowledge Base API."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

# Constants
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes
ALLOWED_CONTENT_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/markdown",
    "text/plain",
]
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".md", ".txt"]


class DocumentBase(BaseModel):
    """Base model for document data.
    
    Attributes:
        filename: Original filename as uploaded by user.
        content_type: MIME type of the uploaded file.
        size: File size in bytes.
    """
    
    filename: str = Field(
        ...,
        description="Original filename",
        examples=["document.pdf", "report.docx", "notes.md", "readme.txt"]
    )
    content_type: str = Field(
        ...,
        description="MIME type of the file",
        examples=["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/markdown", "text/plain"]
    )
    size: int = Field(
        ...,
        description="File size in bytes",
        examples=[1024, 5242880, 10485760]
    )
    
    @field_validator('size')
    @classmethod
    def validate_file_size(cls, v: int) -> int:
        """Validate that file size does not exceed 50MB limit.
        
        Args:
            v: File size in bytes.
            
        Returns:
            int: Validated file size.
            
        Raises:
            ValueError: If file size exceeds 50MB limit.
        """
        if v > MAX_FILE_SIZE:
            raise ValueError(f'File size exceeds maximum limit of 50MB ({MAX_FILE_SIZE} bytes)')
        if v < 0:
            raise ValueError('File size cannot be negative')
        return v
    
    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v: str) -> str:
        """Validate that content type is allowed.
        
        Args:
            v: MIME type string.
            
        Returns:
            str: Validated content type.
            
        Raises:
            ValueError: If content type is not allowed.
        """
        if v not in ALLOWED_CONTENT_TYPES:
            raise ValueError(f'Content type "{v}" is not allowed. Allowed types: {", ".join(ALLOWED_CONTENT_TYPES)}')
        return v


class DocumentCreate(DocumentBase):
    """Model for document upload requests.
    
    Extends DocumentBase with additional fields needed for creation.
    This model is used when accepting file uploads via POST /api/documents.
    """
    pass


class DocumentResponse(DocumentBase):
    """Model for document API responses.
    
    Includes all fields from DocumentBase plus system-generated fields.
    Used in GET and POST responses to return document information.
    
    Attributes:
        id: Unique identifier for the document (UUID).
        filename: Original filename as uploaded by user.
        content_type: MIME type of the uploaded file.
        size: File size in bytes.
        created_at: Timestamp when document was uploaded.
    """
    
    id: str = Field(
        ...,
        description="Unique document identifier (UUID)",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when document was uploaded",
        examples=["2024-01-15T10:30:00Z"]
    )
    
    class Config:
        """Pydantic model configuration."""
        from_attributes = True


class DocumentList(BaseModel):
    """Model for listing endpoint responses.
    
    Contains a list of documents and total count for pagination support.
    Used in GET /api/documents response.
    
    Attributes:
        items: List of document responses.
        total: Total number of documents.
    """
    
    items: List[DocumentResponse] = Field(
        ...,
        description="List of document metadata",
        examples=[[{"id": "550e8400-e29b-41d4-a716-446655440000", "filename": "doc.pdf", "content_type": "application/pdf", "size": 1024, "created_at": "2024-01-15T10:30:00Z"}]]
    )
    total: int = Field(
        ...,
        description="Total number of documents",
        examples=[1, 10, 100]
    )
