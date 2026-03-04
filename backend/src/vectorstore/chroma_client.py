"""ChromaDB vector store client wrapper for the RAG Knowledge Base."""

from typing import List, Optional, Dict, Any
from functools import lru_cache
import chromadb
from chromadb.config import Settings
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection

from src.config import get_settings


class ChromaClient:
    """Wrapper client for ChromaDB vector database operations.
    
    This client provides a clean interface for managing collections
    and performing document embedding storage and retrieval operations.
    
    Attributes:
        persist_dir: Directory path for persistent storage of vector data
        embedding_function: Optional custom embedding function
        
    Example:
        client = ChromaClient(persist_dir="./data/chroma")
        collection = client.get_or_create_collection("my_docs")
        client.add_documents(
            collection_name="my_docs",
            documents=["text content"],
            embeddings=[[0.1, 0.2, ...]],
            ids=["doc1"]
        )
    """
    
    def __init__(self, persist_dir: str, embedding_function=None):
        """Initialize ChromaDB client with persistence.
        
        Args:
            persist_dir: Directory path for storing vector data
            embedding_function: Optional custom embedding function.
                               If None, uses ChromaDB's default.
        """
        self.persist_dir = persist_dir
        self.embedding_function = embedding_function
        self._client: Optional[ClientAPI] = None
        self._collections: Dict[str, Collection] = {}
    
    def _get_client(self) -> ClientAPI:
        """Get or create ChromaDB client instance.
        
        Returns:
            ClientAPI: ChromaDB persistent client.
        """
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                )
            )
        return self._client
    
    def get_or_create_collection(self, name: str) -> Collection:
        """Get existing collection or create a new one.
        
        Args:
            name: Collection name
            
        Returns:
            Collection: ChromaDB collection instance.
            
        Raises:
            ValueError: If collection name is invalid
        """
        if not name or not name.strip():
            raise ValueError("Collection name cannot be empty")
        
        client = self._get_client()
        collection = client.get_or_create_collection(
            name=name,
            embedding_function=self.embedding_function,
        )
        self._collections[name] = collection
        return collection
    
    def delete_collection(self, name: str) -> bool:
        """Delete a collection by name.
        
        Args:
            name: Collection name to delete
            
        Returns:
            bool: True if collection was deleted, False if it didn't exist
        """
        try:
            client = self._get_client()
            client.delete_collection(name=name)
            self._collections.pop(name, None)
            return True
        except Exception:
            # Collection doesn't exist or other error
            return False
    
    def list_collections(self) -> List[str]:
        """List all collection names.
        
        Returns:
            List[str]: List of collection names.
        """
        client = self._get_client()
        collections = client.list_collections()
        return [col.name for col in collections]
    
    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        ids: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> bool:
        """Add documents with embeddings to a collection.
        
        Args:
            collection_name: Name of the collection to add to
            documents: List of document text content
            embeddings: List of embedding vectors (one per document)
            ids: List of unique IDs for each document
            metadatas: Optional list of metadata dictionaries
            
        Returns:
            bool: True if documents were added successfully
            
        Raises:
            ValueError: If collection doesn't exist or inputs are invalid
        """
        try:
            collection = self.get_or_create_collection(collection_name)
            
            collection.add(
                documents=documents,
                embeddings=embeddings,
                ids=ids,
                metadatas=metadatas,
            )
            return True
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
            return False
    
    def query(
        self,
        collection_name: str,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Query a collection with an embedding vector.
        
        Args:
            collection_name: Name of the collection to query
            query_embedding: Query embedding vector
            n_results: Number of results to return (default: 5)
            where: Optional filter conditions
            
        Returns:
            Dict containing ids, documents, embeddings, distances, metadatas
            
        Raises:
            ValueError: If collection doesn't exist
        """
        try:
            collection = self.get_or_create_collection(collection_name)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where,
            )
            
            # Safely extract first result from each list
            ids = results.get("ids", [])
            documents = results.get("documents", [])
            embeddings = results.get("embeddings", [])
            distances = results.get("distances", [])
            metadatas = results.get("metadatas", [])
            
            return {
                "ids": ids[0] if ids else [],
                "documents": documents[0] if documents else [],
                "embeddings": embeddings[0] if embeddings else [],
                "distances": distances[0] if distances else [],
                "metadatas": metadatas[0] if metadatas else [],
            }
        except Exception as e:
            print(f"Error querying ChromaDB: {e}")
            return {
                "ids": [],
                "documents": [],
                "embeddings": [],
                "distances": [],
                "metadatas": [],
            }


@lru_cache()
def get_chroma_client() -> ChromaClient:
    """Get cached ChromaDB client instance.
    
    Returns:
        ChromaClient: Configured ChromaDB client with persistence.
        
    Example:
        client = get_chroma_client()
        collections = client.list_collections()
    """
    settings = get_settings()
    return ChromaClient(persist_dir=settings.CHROMA_PERSIST_DIR)
