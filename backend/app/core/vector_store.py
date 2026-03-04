"""Vector store using ChromaDB for semantic search."""
import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

from app.models.chunk import Chunk, SearchResult
from app.services.embedding_service import EmbeddingService, get_embedding_service

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB-based vector store for document chunks."""
    
    def __init__(self, persist_dir: Optional[str] = None, collection_name: str = "documents"):
        self._persist_dir = persist_dir or os.getenv("CHROMA_PERSIST_DIR", "./data/chromadb")
        self._collection_name = collection_name
        self._embedding_service = get_embedding_service()
        
        os.makedirs(self._persist_dir, exist_ok=True)
        
        self._client = chromadb.PersistentClient(
            path=self._persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"VectorStore initialized: {self._collection_name}")
    
    def add_chunks(self, chunks: List[Chunk], embeddings: List[List[float]]) -> bool:
        """Add chunks with embeddings to the vector store."""
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings length mismatch")
        
        ids = [chunk.id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [{"document_id": c.document_id, "chunk_index": c.chunk_index} for c in chunks]
        
        self._collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        logger.info(f"Added {len(chunks)} chunks")
        return True
    
    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for similar chunks using text query."""
        query_embedding = self._embedding_service.generate_embedding(query)
        
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        search_results = []
        if results['ids'] and results['ids'][0]:
            for i, chunk_id in enumerate(results['ids'][0]):
                distance = results['distances'][0][i]
                similarity = max(0.0, min(1.0, 1.0 - distance))
                
                metadata = results['metadatas'][0][i]
                content = results['documents'][0][i]
                
                chunk = Chunk(
                    id=chunk_id,
                    content=content,
                    document_id=metadata.get('document_id', ''),
                    chunk_index=metadata.get('chunk_index', 0),
                    metadata={}
                )
                
                search_results.append(SearchResult(chunk=chunk, score=similarity))
        
        return search_results
    
    def delete_by_document(self, document_id: str) -> bool:
        """Delete all chunks for a document."""
        results = self._collection.get(where={"document_id": document_id})
        if results['ids']:
            self._collection.delete(ids=results['ids'])
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        return {
            "total_chunks": self._collection.count(),
            "collection_name": self._collection_name,
        }


# Singleton
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get or create the vector store singleton."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
