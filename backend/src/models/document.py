"""Document model for tracking uploaded documents in the RAG Knowledge Base."""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.sqlite import VARCHAR

from src.models.database import Base


class Document(Base):
    """SQLAlchemy model for tracking uploaded documents.
    
    This model stores metadata about documents uploaded to the system,
    including their file information, processing status, and chunking details.
    
    Attributes:
        id: Unique identifier for the document (UUID)
        filename: Original filename as uploaded by user
        file_path: Storage path where the file is saved
        file_type: Document type (pdf, docx, md, txt)
        file_size: File size in bytes
        chunk_count: Number of text chunks created from document
        status: Processing status (uploaded, processing, completed, failed)
        error_message: Error details if processing failed
        uploaded_at: Timestamp when document was uploaded
        processed_at: Timestamp when processing completed
    """
    
    __tablename__ = "documents"
    
    # Primary key - UUID stored as string for SQLite compatibility
    id = Column(VARCHAR(36), primary_key=True, default=lambda: str(uuid4()))
    
    # File information
    filename = Column(String(255), nullable=False)
    file_path = Column(String(511), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx, md, txt, etc.
    file_size = Column(Integer, nullable=False)
    
    # Processing information
    chunk_count = Column(Integer, default=0)
    status = Column(String(50), default="uploaded")  # uploaded, processing, completed, failed
    error_message = Column(String(1023), nullable=True)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        """String representation of the document for debugging."""
        return f"<Document(id='{self.id}', filename='{self.filename}', status='{self.status}')>"
    
    def to_dict(self) -> dict:
        """Convert document to dictionary for JSON serialization.
        
        Returns:
            dict: Document data as a dictionary.
        """
        return {
            "id": self.id,
            "filename": self.filename,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "chunk_count": self.chunk_count,
            "status": self.status,
            "error_message": self.error_message,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
        }
