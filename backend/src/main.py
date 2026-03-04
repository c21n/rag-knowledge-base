"""FastAPI application entry point for the RAG Knowledge Base API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title="RAG Knowledge Base API",
    description="A Retrieval-Augmented Generation (RAG) powered knowledge base API for document processing and intelligent querying.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {"message": "RAG Knowledge Base API", "version": "1.0.0"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
