# Technology Stack

**Project:** Enterprise Intelligent Document Assistant (RAG Knowledge Base)
**Researched:** 2026-03-04

## Recommended Stack

### Core Framework - Backend

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | 3.11+ | Programming language | LangChain ecosystem, AI/ML libraries |
| FastAPI | 0.104+ | Web framework | High performance, async, auto-docs |
| Uvicorn | 0.24+ | ASGI server | Fast, modern Python server |
| Pydantic | 2.5+ | Data validation | Type hints, auto-validation |

### RAG Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| LangChain | 0.1.0+ | RAG orchestration | Industry standard, rich components |
| LangChain-OpenAI | 0.0.5+ | OpenAI integration | Official integration, well-maintained |
| ChromaDB | 0.4.15+ | Vector database | Lightweight, local-first, LangChain native |
| OpenAI Embeddings | latest | Text embeddings | text-embedding-ada-002, proven quality |

### Document Processing

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| PyPDF2 | 3.0.1+ | PDF parsing | Pure Python, no external deps |
| python-docx | 1.1.0+ | Word documents | Clean API, good coverage |
| python-markdown | 3.5.1+ | Markdown | Standard library |
| RecursiveCharacterTextSplitter | LangChain built-in | Text chunking | Smart separators, overlap support |

### Database

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| SQLite | built-in | Relational DB | Zero config, perfect for MVP |
| SQLAlchemy | 2.0.23+ | ORM | Industry standard, async support |
| Alembic | 1.12.1+ | Migrations | SQLAlchemy companion |

### Frontend

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| React | 18.2+ | UI framework | Component-based, ecosystem |
| TypeScript | 5.2+ | Type safety | Catch errors early |
| Vite | 5.0+ | Build tool | Fast dev server, optimized builds |
| Ant Design | 5.12+ | UI components | Enterprise-grade, comprehensive |
| TailwindCSS | 3.3+ | Styling | Utility-first, rapid development |
| Zustand | 4.4+ | State management | Simple, no boilerplate |
| Axios | 1.6+ | HTTP client | Industry standard |

### Infrastructure

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Docker | latest | Containerization | Consistent deployments |
| Docker Compose | latest | Multi-service | Simple local development |
| Nginx | alpine | Reverse proxy | Production-ready static serving |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python-dotenv | 1.0+ | Environment vars | Always for local dev |
| pytest | 7.4+ | Testing | Unit/integration tests |
| black | 23.11+ | Code formatting | Consistent style |
| React Markdown | 9.0+ | Render markdown | Display LLM responses |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Vector DB | ChromaDB | Pinecone/Weaviate | Chroma is local, free, simpler |
| LLM | OpenAI GPT-4 | Claude/GPT-3.5 | GPT-4 best for RAG, good Chinese |
| Backend framework | FastAPI | Flask/Django | FastAPI modern, async, auto-docs |
| Frontend state | Zustand | Redux | Zustand simpler, less boilerplate |
| UI library | Ant Design | Material-UI | Ant Design more enterprise-focused |

## Installation

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Sources

- LangChain Documentation: https://python.langchain.com/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- ChromaDB Documentation: https://docs.trychroma.com/
- Ant Design Documentation: https://ant.design/
