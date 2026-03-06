"""
RAG (Retrieval-Augmented Generation) service for Q&A.
Orchestrates vector search, context assembly, and LLM generation.
"""
import logging
from typing import Optional, List
from datetime import datetime

from app.models.chat import ChatRequest, ChatResponse, SourceCitation
from app.models.chunk import SearchResult
from app.core.vector_store import VectorStore, get_vector_store
from app.core.llm_client import LLMClient, get_llm_client
from app.core.prompt_templates import RAGPromptTemplate, get_rag_prompt

logger = logging.getLogger(__name__)


class RAGService:
    """
    RAG service that combines retrieval and generation.
    
    Workflow:
    1. Search vector store for relevant documents
    2. Format context with prompt template
    3. Generate answer using LLM
    4. Parse citations and return response
    """
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        llm_client: Optional[LLMClient] = None,
        prompt_template: Optional[RAGPromptTemplate] = None
    ):
        """
        Initialize RAG service with dependencies.
        
        Args:
            vector_store: Vector store for document retrieval
            llm_client: LLM client for text generation
            prompt_template: Prompt template for context assembly
        """
        self._vector_store = vector_store or get_vector_store()
        self._llm_client = llm_client or get_llm_client()
        self._prompt_template = prompt_template or get_rag_prompt()
        
        logger.info("RAGService initialized successfully")
    
    def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat request through the RAG pipeline.
        
        Args:
            request: Chat request with query and parameters
            
        Returns:
            ChatResponse with answer and sources
        """
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Retrieve relevant documents
            logger.info(f"Processing query: {request.query[:50]}...")
            search_results = self._retrieve(request.query, top_k=request.top_k)
            
            if not search_results:
                # No relevant documents found
                logger.warning("No relevant documents found for query")
                return self._create_no_results_response(start_time)
            
            # Step 2: Format context and generate prompt
            context = self._format_context(search_results)
            prompt = self._prompt_template.format_prompt(
                query=request.query,
                search_results=search_results,
                include_system_prompt=False
            )
            
            # Step 3: Generate answer using LLM
            logger.info(f"Generating answer with {len(search_results)} documents")
            answer = self._generate(prompt, context)
            
            # Step 4: Extract citations and build response
            citations = self._extract_citations(answer, search_results)
            
            # Calculate response time
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Build and return response
            response = ChatResponse(
                answer=answer,
                sources=citations,
                response_time=response_time,
                retrieved_count=len(search_results)
            )
            
            logger.info(f"Query processed in {response_time:.2f}s")
            return response
            
        except Exception as e:
            logger.error(f"RAG pipeline failed: {e}")
            # Return error response
            response_time = (datetime.utcnow() - start_time).total_seconds()
            return ChatResponse(
                answer=f"抱歉，处理您的问题时出现错误: {str(e)}",
                sources=[],
                response_time=response_time,
                retrieved_count=0
            )
    
    def _retrieve(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Retrieve relevant documents from vector store.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            List of search results
        """
        try:
            return self._vector_store.search(query, top_k=top_k)
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []
    
    def _format_context(self, search_results: List[SearchResult]) -> str:
        """
        Format search results into context string.
        
        Args:
            search_results: List of search results
            
        Returns:
            Formatted context string
        """
        return self._prompt_template.format_context(search_results)
    
    def _generate(self, prompt: str, context: str) -> str:
        """
        Generate answer using LLM.
        
        Args:
            prompt: Formatted prompt
            context: Document context
            
        Returns:
            Generated answer
        """
        try:
            return self._llm_client.generate(prompt, context)
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise RuntimeError(f"无法生成回答: {e}")
    
    def _extract_citations(
        self,
        answer: str,
        search_results: List[SearchResult]
    ) -> List[SourceCitation]:
        """
        Extract source citations from answer and match to search results.
        
        Args:
            answer: Generated answer with citations
            search_results: Search results used for generation
            
        Returns:
            List of source citations
        """
        # Extract document IDs from answer
        cited_doc_ids = self._prompt_template.extract_citations(answer)
        
        if not cited_doc_ids:
            # If no explicit citations, include top sources
            logger.info("No explicit citations found, including top results")
            cited_doc_ids = [r.chunk.document_id for r in search_results[:3]]
        
        # Build citation list
        citations = []
        seen_docs = set()
        
        for result in search_results:
            doc_id = result.chunk.document_id
            
            # Only include cited documents, avoid duplicates
            if doc_id in cited_doc_ids and doc_id not in seen_docs:
                # Create content preview (first 200 chars)
                content_preview = result.chunk.content[:200]
                if len(result.chunk.content) > 200:
                    content_preview += "..."
                
                citation = SourceCitation(
                    document_id=doc_id,
                    chunk_index=result.chunk.chunk_index,
                    content_preview=content_preview,
                    score=result.score
                )
                citations.append(citation)
                seen_docs.add(doc_id)
        
        return citations
    
    def _create_no_results_response(self, start_time: datetime) -> ChatResponse:
        """
        Create response when no relevant documents are found.
        
        Args:
            start_time: Request start time
            
        Returns:
            ChatResponse with no results message
        """
        response_time = (datetime.utcnow() - start_time).total_seconds()
        return ChatResponse(
            answer="抱歉，在知识库中没有找到与您的问题相关的文档。请尝试使用不同的关键词或检查文档是否已上传。",
            sources=[],
            response_time=response_time,
            retrieved_count=0
        )


# Singleton instance for application-wide use
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create the RAG service singleton."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service


def reset_rag_service():
    """Reset the singleton instance (useful for testing)."""
    global _rag_service
    _rag_service = None