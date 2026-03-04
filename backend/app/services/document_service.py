"""Document management service for the RAG Knowledge Base API.

This module provides business logic for document operations including:
- Saving uploaded files to disk
- Retrieving document metadata
- Listing all documents
- Deleting documents from disk and database
"""

import os
import uuid
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.document import Document as DocumentModel
from app.models.document import DocumentResponse

logger = logging.getLogger(__name__)

# Upload directory configuration
UPLOAD_DIR = Path("E:/xinjianwenjianjia/zhishiku/backend/uploads")

# File type mappings
CONTENT_TYPE_MAP = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "text/markdown": "md",
    "text/plain": "txt",
}

FILE_TYPE_MAP = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "md": "text/markdown",
    "txt": "text/plain",
}


class DocumentService:
    """Service class for document management operations.
    
    Handles all business logic related to document uploads, retrieval,
    listing, and deletion. Manages both file storage and database records.
    
    Attributes:
        db: SQLAlchemy database session.
    """
    
    def __init__(self, db: Session):
        """Initialize DocumentService with database session.
        
        Args:
            db: SQLAlchemy database session for database operations.
        """
        self.db = db
    
    def save_document(self, file_content: bytes, filename: str, content_type: str) -> DocumentResponse:
        """Save an uploaded document to storage and database.
        
        Creates a unique ID for the file, saves it to the uploads directory,
        and creates a database record with metadata.
        
        Args:
            file_content: Raw bytes of the uploaded file.
            filename: Original filename as provided by user.
            content_type: MIME type of the uploaded file.
            
        Returns:
            DocumentResponse: Document metadata including generated ID.
            
        Raises:
            IOError: If file cannot be saved to disk.
            SQLAlchemyError: If database record cannot be created.
        """
        # Generate unique ID for the document
        doc_id = str(uuid.uuid4())
        
        # Get file extension from filename
        file_ext = Path(filename).suffix.lower()
        
        # Create storage filename using UUID
        storage_filename = f"{doc_id}{file_ext}"
        
        # Ensure uploads directory exists
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        
        # Full path for saving the file
        file_path = UPLOAD_DIR / storage_filename
        
        try:
            # Save file to disk
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Get file size
            file_size = len(file_content)
            
            # Map content type to file type
            file_type = self._get_file_type(content_type, file_ext)
            
            # Create database record
            db_document = DocumentModel(
                id=doc_id,
                filename=filename,
                file_path=str(file_path),
                file_type=file_type,
                file_size=file_size,
                status="uploaded",
                chunk_count=0,
                uploaded_at=datetime.utcnow()
            )
            
            self.db.add(db_document)
            self.db.commit()
            self.db.refresh(db_document)
            
            logger.info(f"Document saved: id={doc_id}, filename={filename}, size={file_size}")
            
            # Return DocumentResponse
            return DocumentResponse(
                id=doc_id,
                filename=filename,
                content_type=content_type,
                size=file_size,
                created_at=db_document.uploaded_at
            )
            
        except Exception as e:
            # Rollback on error and remove file if created
            self.db.rollback()
            if file_path.exists():
                file_path.unlink()
            logger.error(f"Failed to save document: {e}")
            raise
    
    def get_document(self, doc_id: str) -> Optional[DocumentResponse]:
        """Retrieve document metadata by ID.
        
        Args:
            doc_id: Unique document identifier.
            
        Returns:
            DocumentResponse: Document metadata if found, None otherwise.
        """
        db_document = self.db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        
        if not db_document:
            logger.warning(f"Document not found: id={doc_id}")
            return None
        
        # Map file_type back to content_type
        content_type = self._get_content_type(db_document.file_type)
        
        return DocumentResponse(
            id=db_document.id,
            filename=db_document.filename,
            content_type=content_type,
            size=db_document.file_size,
            created_at=db_document.uploaded_at
        )
    
    def list_documents(self) -> List[DocumentResponse]:
        """List all documents with metadata from database.
        
        Returns:
            List[DocumentResponse]: List of all document metadata.
        """
        db_documents = self.db.query(DocumentModel).order_by(DocumentModel.uploaded_at.desc()).all()
        
        documents = []
        for db_doc in db_documents:
            content_type = self._get_content_type(db_doc.file_type)
            documents.append(DocumentResponse(
                id=db_doc.id,
                filename=db_doc.filename,
                content_type=content_type,
                size=db_doc.file_size,
                created_at=db_doc.uploaded_at
            ))
        
        logger.info(f"Listed {len(documents)} documents")
        return documents
    
    def delete_document(self, doc_id: str) -> bool:
        """Remove document from disk and database.
        
        Deletes both the physical file from storage and the metadata
        record from the database.
        
        Args:
            doc_id: Unique document identifier.
            
        Returns:
            bool: True if deletion successful, False if document not found.
            
        Raises:
            IOError: If file cannot be deleted from disk.
            SQLAlchemyError: If database record cannot be deleted.
        """
        db_document = self.db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        
        if not db_document:
            logger.warning(f"Document not found for deletion: id={doc_id}")
            return False
        
        try:
            # Delete file from disk if it exists
            file_path = Path(db_document.file_path)
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Deleted file: {file_path}")
            
            # Delete database record
            self.db.delete(db_document)
            self.db.commit()
            
            logger.info(f"Document deleted: id={doc_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete document: {e}")
            raise
    
    def _get_file_type(self, content_type: str, file_ext: str) -> str:
        """Map content type or extension to file type string.
        
        Args:
            content_type: MIME type of the file.
            file_ext: File extension.
            
        Returns:
            str: File type string (pdf, docx, md, txt).
        """
        return CONTENT_TYPE_MAP.get(content_type, file_ext.lstrip('.'))
    
    def _get_content_type(self, file_type: str) -> str:
        """Map file type to content type.
        
        
            file_type: File type string (pdf, docx, md, txt).
            
        Returns:
            str: MIME type string.
        """
        return FILE_TYPE_MAP.get(file_type.lower() if file_type else "", "application/octet-stream")
