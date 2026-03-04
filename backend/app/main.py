"""FastAPI application entry point for the RAG Knowledge Base API."""

import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.documents import router as documents_router
from app.api.routes.processing import router as processing_router
from app.api.routes.search import router as search_router
from app.api.routes.processing import router as processing_router
from app.api.routes.search import router as search_router
from app.api.routes.processing import router as processing_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Knowledge Base API",
    description="A Retrieval-Augmented Generation (RAG) powered knowledge base API.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(processing_router)
app.include_router(search_router)
app.include_router(documents_router)
app.include_router(processing_router)
app.include_router(search_router, prefix="/api")
app.include_router(documents_router)
app.include_router(processing_router)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {"message": "RAG Knowledge Base API", "version": "1.0.0"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    upload_dir = Path("E:/xinjianwenjianjia/zhishiku/backend/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Uploads directory ready: {upload_dir}")
    
    routes = [r.path for r in app.routes if hasattr(r, 'path')]
    api_routes = sorted([r for r in routes if r.startswith('/api')])
    logger.info("Available API routes:")
    for route in api_routes:
        logger.info(f"  {route}")
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Application shutdown initiated")
