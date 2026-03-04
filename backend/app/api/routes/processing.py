"""FastAPI routes for document processing operations."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.models.database import get_db
from src.models.document import Document as DocumentModel
from app.services.document_service import DocumentService
from app.services.document_processor import DocumentProcessor, ProcessingStatus

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/documents",
    tags=["documents", "processing"],
)


def get_processor(db: Session = Depends(get_db)) -> DocumentProcessor:
    return DocumentProcessor(db=db)


def get_doc_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(db)


@router.post("/{document_id}/process", summary="Process document")
async def process_document(
    document_id: str,
    processor: DocumentProcessor = Depends(get_processor),
    service: DocumentService = Depends(get_doc_service),
):
    """Trigger document processing to extract text and create chunks."""
    document = service.get_document(document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id '{document_id}' not found"
        )
    
    try:
        doc_model = processor.db.query(DocumentModel).filter(
            DocumentModel.id == document_id
        ).first()
        
        if doc_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found in database"
            )
        
        file_path = doc_model.file_path
        chunks = processor.process_document(document_id, file_path)
        
        return {
            "document_id": document_id,
            "status": ProcessingStatus.COMPLETED,
            "chunk_count": len(chunks),
            "message": "Document processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing failed: {str(e)}"
        )


@router.get("/{document_id}/status", summary="Get processing status")
async def get_status(
    document_id: str,
    processor: DocumentProcessor = Depends(get_processor),
):
    """Get the current processing status of a document."""
    status_info = processor.get_processing_status(document_id)
    
    if status_info.get("status") == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id '{document_id}' not found"
        )
    
    return status_info


@router.post("/{document_id}/process/background", summary="Process in background")
async def process_document_background(
    document_id: str,
    background_tasks: BackgroundTasks,
    processor: DocumentProcessor = Depends(get_processor),
    service: DocumentService = Depends(get_doc_service),
):
    """Trigger document processing as a background task."""
    document = service.get_document(document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id '{document_id}' not found"
        )
    
    doc_model = processor.db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()
    
    if doc_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found in database"
        )
    
    def _process_bg(doc_id: str, file_path: str):
        try:
            proc = DocumentProcessor(db=processor.db)
            proc.process_document(doc_id, file_path)
        except Exception as e:
            logger.error(f"Background processing failed for {doc_id}: {e}")
    
    background_tasks.add_task(_process_bg, document_id, doc_model.file_path)
    
    return {
        "document_id": document_id,
        "status": ProcessingStatus.PROCESSING,
        "message": "Processing started in background"
    }
