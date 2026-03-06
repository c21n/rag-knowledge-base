"""
Chat API routes for RAG-based Q&A.
"""
import logging
import time
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends

from app.models.chat import ChatRequest, ChatResponse, SourceCitation
from app.services.rag_service import get_rag_service, RAGService
from app.services.role_service import get_role_service, RoleService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
    role_service: RoleService = Depends(get_role_service)
):
    """
    Process a chat query using RAG.
    
    Args:
        request: Chat request with query and parameters
        
    Returns:
        ChatResponse with answer and source citations
    """
    start_time = time.time()
    
    try:
        # Validate role if provided
        if request.role_id:
            role = role_service.get_role(request.role_id)
            if not role:
                raise HTTPException(status_code=404, detail=f"Role '{request.role_id}' not found")
        
        # Process query through RAG pipeline
        logger.info(f"Processing chat query: {request.query[:50]}...")
        response = rag_service.chat(request)
        
        # Update response time
        response.response_time = time.time() - start_time
        
        logger.info(f"Chat response generated in {response.response_time:.2f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")


@router.get("/api/chat/history/{session_id}")
async def get_chat_history(
    session_id: str,
    limit: int = 50
):
    """
    Get chat history for a session.
    
    Args:
        session_id: Session identifier
        limit: Maximum number of messages to return
        
    Returns:
        List of chat messages
    """
    # TODO: Implement after conversation service is ready
    return {
        "session_id": session_id,
        "messages": [],
        "total": 0
    }


@router.post("/api/chat/feedback")
async def submit_feedback(
    message_id: str,
    feedback_type: str,  # 'thumbs_up' or 'thumbs_down'
    comment: Optional[str] = None
):
    """
    Submit feedback for a chat message.
    
    Args:
        message_id: Message identifier
        feedback_type: Type of feedback ('thumbs_up' or 'thumbs_down')
        comment: Optional comment
        
    Returns:
        Success confirmation
    """
    if feedback_type not in ['thumbs_up', 'thumbs_down']:
        raise HTTPException(status_code=400, detail="Invalid feedback type")
    
    # TODO: Store feedback
    logger.info(f"Feedback received: {feedback_type} for message {message_id}")
    
    return {"status": "success", "message": "Feedback recorded"}
