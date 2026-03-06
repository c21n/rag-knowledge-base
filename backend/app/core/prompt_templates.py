"""
RAG prompt templates for assembling context and generating answers.
Supports Chinese language with source citations.
"""
import logging
from typing import List, Optional
from app.models.chunk import SearchResult

logger = logging.getLogger(__name__)


class RAGPromptTemplate:
    """Template for RAG prompts with context assembly and citation support."""
    
    def __init__(
        self,
        system_prompt: Optional[str] = None,
        context_format: Optional[str] = None,
        citation_format: Optional[str] = None
    ):
        """
        Initialize RAG prompt template.
        
        Args:
            system_prompt: Custom system prompt (defaults to Chinese RAG prompt)
            context_format: Custom context format string
            citation_format: Custom citation format string
        """
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        self.context_format = context_format or self._get_default_context_format()
        self.citation_format = citation_format or "[source: {document_id}]"
    
    def _get_default_system_prompt(self) -> str:
        """Get default system prompt in Chinese."""
        return """你是一个企业知识库助手。你的任务是基于提供的参考文档准确回答用户问题。

请遵循以下准则：
1. 仅基于参考文档中的信息回答问题，不要添加文档中未提及的内容
2. 如果参考文档中没有相关信息，请明确说明"参考文档中没有找到相关信息"
3. 在回答中标注信息来源，格式为 [source: document_id]
4. 保持回答简洁、准确、专业
5. 如果多个文档提供相关信息，可以综合回答并分别标注来源"""
    
    def _get_default_context_format(self) -> str:
        """Get default context format for documents."""
        return """【文档 {index}】(ID: {document_id}, 相似度: {score:.2%})
{content}

"""
    
    def format_context(self, search_results: List[SearchResult]) -> str:
        """
        Format search results into context string.
        
        Args:
            search_results: List of search results from vector store
            
        Returns:
            Formatted context string with document citations
        """
        if not search_results:
            return "无参考文档"
        
        context_parts = []
        
        for idx, result in enumerate(search_results, start=1):
            # Format each document with metadata
            doc_text = self.context_format.format(
                index=idx,
                document_id=result.chunk.document_id,
                score=result.score,
                content=result.chunk.content
            )
            context_parts.append(doc_text)
        
        return "".join(context_parts)
    
    def format_prompt(
        self,
        query: str,
        search_results: List[SearchResult],
        include_system_prompt: bool = True
    ) -> str:
        """
        Format complete RAG prompt with query and context.
        
        Args:
            query: User question
            search_results: List of search results from vector store
            include_system_prompt: Whether to include system prompt
            
        Returns:
            Complete formatted prompt
        """
        context = self.format_context(search_results)
        
        prompt_parts = []
        
        if include_system_prompt:
            prompt_parts.append(self.system_prompt)
            prompt_parts.append("\n\n")
        
        prompt_parts.append("参考文档:\n")
        prompt_parts.append(context)
        prompt_parts.append("\n用户问题: ")
        prompt_parts.append(query)
        prompt_parts.append("\n\n请基于参考文档回答问题，并在回答中标注来源 [source: document_id]:")
        
        return "".join(prompt_parts)
    
    def extract_citations(self, response: str) -> List[str]:
        """
        Extract document IDs from citations in the response.
        
        Args:
            response: LLM generated response with citations
            
        Returns:
            List of document IDs mentioned in citations
        """
        import re
        
        # Find all [source: document_id] patterns
        pattern = r'\[source:\s*([^\]]+)\]'
        citations = re.findall(pattern, response)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_citations = []
        for doc_id in citations:
            doc_id = doc_id.strip()
            if doc_id not in seen:
                seen.add(doc_id)
                unique_citations.append(doc_id)
        
        return unique_citations


# Singleton instance for application-wide use
_rag_prompt_template: Optional[RAGPromptTemplate] = None


def get_rag_prompt() -> RAGPromptTemplate:
    """Get or create the RAG prompt template singleton."""
    global _rag_prompt_template
    if _rag_prompt_template is None:
        _rag_prompt_template = RAGPromptTemplate()
    return _rag_prompt_template


def reset_rag_prompt():
    """Reset the singleton instance (useful for testing)."""
    global _rag_prompt_template
    _rag_prompt_template = None