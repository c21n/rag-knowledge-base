"""
Semantic search API endpoints.
"""
import logging
from typing import List
from fastapi import APIRouter, HTTPException, status

from app.models.chunk import SearchRequest, SearchResponse, SearchResult
from app.core.vector_store import get_vector_store

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["search"])


@router.post(
    "",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Semantic search",
    description="Search for relevant document chunks using semantic similarity."
)
async def search_documents(request: SearchRequest):
    """
    Perform semantic search across all processed documents.
    
    Args:
        request: Search request with query and optional top_k parameter
        
    Returns:
        SearchResponse with matching chunks and similarity scores
        
    Raises:
        HTTPException: If search fails
    """
    try:
        logger.info(f"Search query: '{request.query}' (top_k={request.top_k})")
        
        # Get vector store and perform search
        vector_store = get_vector_store()
        results = vector_store.search(request.query, top_k=request.top_k)
        
        logger.info(f"Search returned {len(results)} results")
        
        return SearchResponse(
            query=request.query,
            results=results,
            total_results=len(results)
        )
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get(
    "/stats",
    summary="Vector store statistics",
    description="Get statistics about the vector store."
)
async def get_vector_stats():
    """
    Get vector store statistics.
    
    Returns:
        Dictionary with collection stats
    """
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )