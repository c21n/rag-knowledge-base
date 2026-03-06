"""Conversation service for managing chat history."""

import logging
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.conversation import Conversation, Message
from src.models.database import get_db

logger = logging.getLogger(__name__)


class ConversationService:
    """Service for managing conversation history."""
    
    def __init__(self, db: Session):
        """Initialize conversation service.
        
        Args:
            db: SQLAlchemy database session.
        """
        self.db = db
    
    def get_or_create_conversation(self, session_id: str) -> Conversation:
        """Get or create a conversation by session ID.
        
        Args:
            session_id: Session identifier.
            
        Returns:
            Conversation object.
        """
        conv = self.db.query(Conversation).filter_by(session_id=session_id).first()
        if not conv:
            conv = Conversation(session_id=session_id)
            self.db.add(conv)
            self.db.commit()
            self.db.refresh(conv)
            logger.info(f"Created new conversation for session {session_id}")
        return conv
    
    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        role_template_id: Optional[str] = None,
        sources: Optional[List[dict]] = None
    ) -> Message:
        """Save a message to conversation history.
        
        Args:
            session_id: Session identifier.
            role: Message role ('user' or 'assistant').
            content: Message content.
            role_template_id: Optional role template ID.
            sources: Optional source citations.
            
        Returns:
            Saved Message object.
        """
        try:
            conv = self.get_or_create_conversation(session_id)
            msg = Message(
                conversation_id=conv.id,
                role=role,
                content=content,
                role_template_id=role_template_id,
                sources=sources
            )
            self.db.add(msg)
            conv.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(msg)
            logger.info(f"Saved {role} message for session {session_id}")
            return msg
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to save message: {e}")
            raise
    
    def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Message]:
        """Get conversation history for a session.
        
        Args:
            session_id: Session identifier.
            limit: Maximum number of messages to return.
            
        Returns:
            List of messages in chronological order.
        """
        conv = self.db.query(Conversation).filter_by(session_id=session_id).first()
        if not conv:
            return []
        
        return self.db.query(Message) \
            .filter_by(conversation_id=conv.id) \
            .order_by(Message.created_at.asc()) \
            .limit(limit) \
            .all()
    
    def get_recent_conversations(self, limit: int = 10) -> List[Conversation]:
        """Get recent conversations.
        
        Args:
            limit: Maximum number of conversations to return.
            
        Returns:
            List of conversations ordered by most recent first.
        """
        return self.db.query(Conversation) \
            .order_by(Conversation.updated_at.desc()) \
            .limit(limit) \
            .all()


# Dependency function for FastAPI
def get_conversation_service(db: Session = next(get_db())) -> ConversationService:
    """Get conversation service instance.
    
    Args:
        db: Database session from dependency.
        
    Returns:
        ConversationService instance.
    """
    return ConversationService(db)
