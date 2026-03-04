"""Document processor service for text extraction and chunking.

This module provides the DocumentProcessor service that:
- Extracts text from documents using format-specific loaders
- Splits text into chunks using LangChain RecursiveCharacterTextSplitter
- Tracks processing status for each document
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.document_loaders import get_loader
from src.models.document import Document as DocumentModel

logger = logging.getLogger(__name__)
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.document_loaders import get_loader
from src.models.document import Document as DocumentModel

logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """Represents a single chunk of text from a document."""
    page_content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {"page_content": self.page_content, "metadata": self.metadata}


class ProcessingStatus:
    """Processing status values."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentProcessor:
    """Service for processing documents into text chunks."""
    
    def __init__(self, db=None, chunk_size: int = 500, chunk_overlap: int = 50):
        self.db = db
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._text_splitter = None
    
    @property
    def text_splitter(self):
        if self._text_splitter is None:
            self._text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
        return self._text_splitter
    
    def process_document(self, document_id: str, file_path: str, store_embeddings: bool = True) -> List[DocumentChunk]:
        """Process a document and return text chunks. Optionally generate and store embeddings."""
        logger.info(f"Processing document: id={document_id}, path={file_path}")
        self._update_status(document_id, ProcessingStatus.PROCESSING)
        
        try:
            from pathlib import Path
            ext = Path(file_path).suffix.lower()
            loader = get_loader(ext)
            if loader is None:
                raise ValueError(f"Unsupported file format: {ext}")
            
            text = loader(file_path)
            if not text:
                raise ValueError("Failed to extract text from document")
            
            logger.info(f"Extracted {len(text)} characters")
            chunks = self.create_chunks(text, document_id)
            logger.info(f"Created {len(chunks)} chunks")
            
            # Generate and store embeddings if requested
            if store_embeddings and chunks:
                try:
                    self._store_chunks_with_embeddings(document_id, chunks)
                    logger.info(f"Stored {len(chunks)} chunks with embeddings")
                except Exception as e:
                    logger.error(f"Failed to store embeddings: {e}")
                    # Continue without embeddings - don't fail the whole process
            
            self._update_status(document_id, ProcessingStatus.COMPLETED, chunk_count=len(chunks))
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to process document {document_id}: {e}")
            self._update_status(document_id, ProcessingStatus.FAILED, error_message=str(e))
            raise
        """Process a document and return text chunks."""
        logger.info(f"Processing document: id={document_id}, path={file_path}")
        self._update_status(document_id, ProcessingStatus.PROCESSING)
        
        try:
            from pathlib import Path
            ext = Path(file_path).suffix.lower()
            loader = get_loader(ext)
            if loader is None:
                raise ValueError(f"Unsupported file format: {ext}")
            
            text = loader(file_path)
            if not text:
                raise ValueError("Failed to extract text from document")
            
            logger.info(f"Extracted {len(text)} characters")
            chunks = self.create_chunks(text, document_id)
            logger.info(f"Created {len(chunks)} chunks")
            
            self._update_status(document_id, ProcessingStatus.COMPLETED, chunk_count=len(chunks))
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to process document {document_id}: {e}")
            self._update_status(document_id, ProcessingStatus.FAILED, error_message=str(e))
            raise
    
    def create_chunks(self, text: str, doc_id: str, 
                      chunk_size: Optional[int] = None,
                      chunk_overlap: Optional[int] = None) -> List[DocumentChunk]:
        """Split text into chunks with metadata."""
        size = chunk_size or self.chunk_size
        overlap = chunk_overlap or self.chunk_overlap
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        
        langchain_docs = splitter.split_text(text)
        total_chunks = len(langchain_docs)
        chunks = []
        
        for index, content in enumerate(langchain_docs):
            chunk = DocumentChunk(
                page_content=content,
                metadata={
                    "source_doc_id": doc_id,
                    "chunk_index": index,
                    "total_chunks": total_chunks,
                    "chunk_size": len(content),
                }
            )
            chunks.append(chunk)
        
        return chunks
    
    def get_processing_status(self, document_id: str) -> Dict[str, Any]:
        """Get the processing status for a document."""
        if self.db is None:
            return {"status": ProcessingStatus.PENDING, "error": "No database connection"}
        
        try:
            doc = self.db.query(DocumentModel).filter(
                DocumentModel.id == document_id
            ).first()
            
            if doc is None:
                return {"status": "not_found", "error": "Document not found"}
            
            return {
                "document_id": document_id,
                "status": doc.status,
                "chunk_count": doc.chunk_count,
                "error_message": doc.error_message,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _update_status(self, document_id: str, status: str,
                       chunk_count: Optional[int] = None,
                       error_message: Optional[str] = None) -> bool:
        """Update processing status in database."""
        if self.db is None:
            return False
        
        try:
            doc = self.db.query(DocumentModel).filter(
                DocumentModel.id == document_id
            ).first()
            
            if doc is None:
                return False
            
            doc.status = status
            if chunk_count is not None:
                doc.chunk_count = chunk_count
            if error_message is not None:
                doc.error_message = error_message
            if status == ProcessingStatus.COMPLETED:
                doc.processed_at = datetime.utcnow()
            
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to update status: {e}")
            self.db.rollback()
            return False
    
    def _store_chunks_with_embeddings(self, document_id: str, chunks: List[DocumentChunk]) -> bool:
        """Generate embeddings and store chunks in vector store."""
        from app.services.embedding_service import get_embedding_service
        from app.core.vector_store import get_vector_store
        from app.models.chunk import Chunk
        import uuid
        
        # Get services
        embedding_service = get_embedding_service()
        vector_store = get_vector_store()
        
        # Prepare chunks and texts
        chunk_models = []
        texts = []
        
        for i, doc_chunk in enumerate(chunks):
            chunk_model = Chunk(
                id=str(uuid.uuid4()),
                content=doc_chunk.page_content,
                document_id=document_id,
                chunk_index=i,
                metadata=doc_chunk.metadata
            )
            chunk_models.append(chunk_model)
            texts.append(doc_chunk.page_content)
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(texts)} chunks")
        embeddings = embedding_service.generate_embeddings(texts)
        
        # Store in vector store
        vector_store.add_chunks(chunk_models, embeddings)
        logger.info(f"Successfully stored {len(chunk_models)} chunks in vector store")
        
        return True
    
    def reprocess_document(self, document_id: str, file_path: str) -> List[DocumentChunk]:
        """Re-process a document, deleting old embeddings first."""
        logger.info(f"Reprocessing document: {document_id}")
        
        # Delete old embeddings
        try:
            from app.core.vector_store import get_vector_store
            vector_store = get_vector_store()
            vector_store.delete_by_document(document_id)
            logger.info(f"Deleted old embeddings for document {document_id}")
        except Exception as e:
            logger.warning(f"Failed to delete old embeddings: {e}")
        
        # Process again
        return self.process_document(document_id, file_path, store_embeddings=True)
