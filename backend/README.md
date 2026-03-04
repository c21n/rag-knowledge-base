# RAG Knowledge Base Backend

FastAPI backend for the RAG-powered Knowledge Base application.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration, especially OPENAI_API_KEY
   ```

## Environment Setup

Copy `.env.example` to `.env` and configure the following variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `DATABASE_URL` | SQLite database connection string | `sqlite:///./data/app.db` |
| `CHROMA_PERSIST_DIR` | ChromaDB persistence directory | `./data/chroma` |
| `UPLOAD_DIR` | Directory for uploaded files | `./data/uploads` |
| `EMBEDDING_MODEL` | OpenAI embedding model | `text-embedding-ada-002` |
| `CHUNK_SIZE` | Text chunk size for processing | `500` |
| `CHUNK_OVERLAP` | Overlap between chunks | `50` |

## Running the Server

### Development Mode (with auto-reload)

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, access the auto-generated API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint - API info |
| `GET` | `/api/health` | Health check endpoint |

## Testing

Run the test suite:

```bash
pytest
```

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── config.py      # Configuration management
│   └── main.py        # FastAPI application
├── data/
│   ├── uploads/       # Uploaded documents
│   └── chroma/        # Vector database
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
├── .gitignore
├── pyproject.toml
└── README.md
```
