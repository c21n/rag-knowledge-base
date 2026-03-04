# Architecture Patterns

**Domain:** RAG Knowledge Base System
**Researched:** 2026-03-04

## Recommended Architecture

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│  (React + TypeScript + Ant Design)  │
│  - ChatInterface component          │
│  - DocumentManager component        │
│  - PromptTemplateManager            │
├─────────────────────────────────────┤
│          API Gateway Layer          │
│  (FastAPI + Uvicorn)                │
│  - /api/chat (Q&A endpoint)         │
│  - /api/documents (CRUD)            │
│  - /api/config (templates)          │
├─────────────────────────────────────┤
│        Business Logic Layer         │
│  (LangChain + Custom Services)      │
│  - RAGService (orchestration)       │
│  - DocumentService (processing)     │
│  - LLMService (generation)          │
├─────────────────────────────────────┤
│         Data Access Layer           │
│  - ChromaDB (vector storage)        │
│  - SQLite (relational data)         │
│  - Local filesystem (raw files)     │
└─────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| ChatInterface | User chat UI | API Gateway (HTTP) |
| DocumentManager | Upload/list/delete | API Gateway (HTTP) |
| FastAPI Routes | Request handling | Services |
| RAGService | RAG pipeline orchestration | DocumentService, LLMService |
| DocumentService | Vector store operations | ChromaDB, TextSplitter |
| LLMService | LLM interactions | OpenAI API |
| TextSplitter | Document chunking | DocumentService |
| ChromaDB | Vector similarity search | DocumentService |

### Data Flow

**Document Upload Flow:**
```
User selects file → Frontend upload → FastAPI receives → Save to disk
                                        ↓
                              DocumentLoader parses
                                        ↓
                              TextSplitter chunks
                                        ↓
                              Embedding model → ChromaDB store
```

**Question/Answer Flow:**
```
User types question → Frontend POST /api/chat → RAGService
                                        ↓
                              Question → Embedding → ChromaDB search
                                        ↓
                              Top-K chunks retrieved
                                        ↓
                              Build prompt with context
                                        ↓
                              LLM generates answer
                                        ↓
                              Return answer + sources
                                        ↓
                              Save to conversation history
```

## Patterns to Follow

### Pattern 1: Dependency Injection
**What:** Services receive dependencies via constructor
**When:** All service classes
**Why:** Testability, flexibility to swap implementations

```python
class RAGService:
    def __init__(self, document_service: DocumentService, llm_service: LLMService):
        self.document_service = document_service
        self.llm_service = llm_service
```

### Pattern 2: Repository Pattern
**What:** Abstract data access behind service interfaces
**When:** Database operations
**Why:** Swap SQLite for PostgreSQL later without changing business logic

### Pattern 3: Chain of Responsibility (LangChain)
**What:** Compose processing steps as chainable operations
**When:** RAG pipeline
**Why:** Readable, testable, easy to modify

```python
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

### Pattern 4: Frontend Container/Presentational
**What:** Separate data fetching from UI rendering
**When:** React components
**Why:** Reusable UI, testable logic

## Anti-Patterns to Avoid

### Anti-Pattern 1: God Service
**What:** One service class handling everything
**Why bad:** Unmaintainable, hard to test
**Instead:** Split into focused services (RAG, Document, LLM)

### Anti-Pattern 2: Direct DB Access from Routes
**What:** FastAPI routes querying database directly
**Why bad:** Business logic leaks, hard to change DB
**Instead:** Routes call services, services handle persistence

### Anti-Pattern 3: Frontend State in LocalStorage
**What:** Storing chat history in browser storage
**Why bad:** Lost on logout, size limits
**Instead:** Backend persistence with SQLite

### Anti-Pattern 4: Synchronous LLM Calls
**What:** Blocking while waiting for LLM response
**Why bad:** Poor UX, timeout issues
**Instead:** Streaming responses or async with loading states

## Scalability Considerations

| Concern | At 10 users | At 100 users | At 1000 users |
|---------|-------------|--------------|---------------|
| Vector search | ChromaDB local | ChromaDB persistent | Pinecone/Weaviate cloud |
| Database | SQLite | PostgreSQL | PostgreSQL + connection pool |
| LLM API | OpenAI direct | OpenAI direct | Azure OpenAI for rate limits |
| File storage | Local disk | Local disk | S3/MinIO |
| Deployment | Docker Compose | Docker Compose + Nginx | Kubernetes |

## Build Order Recommendations

1. **Backend foundation** - FastAPI structure, config, logging
2. **Database models** - SQLAlchemy models, migrations
3. **Document processing** - Loaders, splitters, embeddings
4. **Vector store** - ChromaDB integration
5. **RAG pipeline** - Chain assembly, prompt templates
6. **API endpoints** - Routes, validation
7. **Frontend foundation** - Vite + React setup
8. **Chat UI** - Basic chat interface
9. **Document management UI** - Upload, list
10. **Integration** - Connect frontend to backend
11. **Polish** - Error handling, loading states
12. **Docker** - Containerization

## Sources

- LangChain Architecture patterns
- FastAPI best practices
- Clean Architecture principles
- Enterprise RAG system patterns
