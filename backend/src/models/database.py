"""SQLAlchemy database infrastructure for the RAG Knowledge Base API."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

from src.config import get_settings


# Initialize settings
settings = get_settings()

# Create SQLAlchemy engine
# SQLite doesn't need connection pooling for single-user applications
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def get_db():
    """Dependency function for FastAPI to get database session.
    
    Yields:
        Session: SQLAlchemy database session.
        
    Usage:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db session here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables from defined models.
    
    This should be called once on application startup to ensure
    all tables exist. For production, use Alembic migrations.
    """
    Base.metadata.create_all(bind=engine)


@lru_cache()
def get_engine():
    """Get cached database engine instance.
    
    Returns:
        Engine: SQLAlchemy engine instance.
    """
    return engine
