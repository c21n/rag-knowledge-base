"""FastAPI routes for document management operations."""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.models.document import Document as DocumentModel
from app.services.document_service import DocumentService
from app.services.document_processor import DocumentProcessor, ProcessingStatus
from app.models.document import DocumentResponse, DocumentList, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
)


def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(db)


def get_processor(db: Session = Depends(get_db)) -> DocumentProcessor:
    return DocumentProcessor(db=db)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload document",
)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload"),
    process: bool = Query(True, description="Whether to process document after upload"),
    background_tasks: BackgroundTasks = None,
    service: DocumentService = Depends(get_document_service),
    processor: DocumentProcessor = Depends(get_processor),
):
    """Upload a document to the knowledge base."""
    file_ext = ""
    if file.filename:
        file_ext = "." + file.filename.split(".")[-1].lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Invalid file type rejected: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    content = await file.read()
    file_size = len(content)
    
    if file_size > MAX_FILE_SIZE:
        logger.warning(f"File too large rejected: {file.filename}, size={file_size}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of 50MB"
        )
    
    if file_size == 0:
        logger.warning(f"Empty file rejected: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )
    
    logger.info(f"Uploading document: {file.filename}, type={file.content_type}, size={file_size}")
    
    try:
        response = service.save_document(
            file_content=content,
            filename=file.filename or "unnamed_file",
            content_type=file.content_type or "application/octet-stream"
        )
        logger.info(f"Document uploaded successfully: id={response.id}")
        
        if process and background_tasks:
            doc_model = processor.db.query(DocumentModel).filter(
                DocumentModel.id == response.id
            ).first()
            
            if doc_model:
                def _process_bg(doc_id: str, file_path: str):
                    try:
                        proc = DocumentProcessor(db=processor.db)
                        proc.process_document(doc_id, file_path)
                    except Exception as e:
                        logger.error(f"Background processing failed for {doc_id}: {e}")
                
                background_tasks.add_task(_process_bg, response.id, doc_model.file_path)
                logger.info(f"Background processing scheduled for document: {response.id}")
        
        result = response.model_dump() if hasattr(response, 'model_dump') else response.dict()
        result['processing_status'] = ProcessingStatus.PROCESSING if process else ProcessingStatus.PENDING
        return result
        
    except Exception as e:
        logger.error(f"Failed to upload document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save document: {str(e)}"
        )


@router.get("", response_model=DocumentList, summary="List all documents")
async def list_documents(service: DocumentService = Depends(get_document_service)):
    """List all uploaded documents."""
    documents = service.list_documents()
    logger.info(f"Listing documents: total={len(documents)}")
    
    return DocumentList(items=documents, total=len(documents))


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete document")
async def delete_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service)
):
    """Delete a document by ID."""
    logger.info(f"Deleting document: id={document_id}")
    
    try:
        success = service.delete_document(document_id)
        
        if not success:
            logger.warning(f"Document not found for deletion: id={document_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with id '{document_id}' not found"
            )
        
        logger.info(f"Document deleted successfully: id={document_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {str(e)}"
        )
