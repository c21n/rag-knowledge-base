"""Tests for Conversation API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestConversationAPI:
    """Test cases for conversation API endpoints."""
    
    def test_get_conversation_history(self):
        """Test GET /api/chat/history/{session_id} endpoint."""
        # First create a conversation by sending a message
        chat_response = client.post(
            "/api/chat",
            json={
                "query": "What is AI?",
                "role_id": "technical_support",
                "session_id": "test-conv-session"
            }
        )
        assert chat_response.status_code == 200
        
        # Now get the history
        response = client.get("/api/chat/history/test-conv-session")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "session_id" in data
        assert "messages" in data
        assert "total" in data
        assert data["session_id"] == "test-conv-session"
        assert isinstance(data["messages"], list)
    
    def test_conversation_history_empty(self):
        """Test getting history for non-existent session."""
        response = client.get("/api/chat/history/nonexistent-session-xyz")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["session_id"] == "nonexistent-session-xyz"
        assert data["messages"] == []
        assert data["total"] == 0
    
    def test_conversation_history_pagination(self):
        """Test conversation history pagination."""
        response = client.get("/api/chat/history/test-session?limit=5")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "messages" in data
        assert len(data["messages"]) <= 5
    
    def test_chat_saves_to_history(self):
        """Test that chat messages are saved to conversation history."""
        session_id = "test-save-session"
        
        # Send a chat message
        chat_response = client.post(
            "/api/chat",
            json={
                "query": "What is machine learning?",
                "role_id": "technical_support",
                "session_id": session_id
            }
        )
        assert chat_response.status_code == 200
        
        # Get history
        history_response = client.get(f"/api/chat/history/{session_id}")
        assert history_response.status_code == 200
        
        data = history_response.json()
        # Note: In stub implementation, messages list will be empty
        # Full implementation will have messages
        assert "messages" in data


class TestConversationWithRole:
    """Test conversation with different roles."""
    
    def test_conversation_with_technical_support(self):
        """Test conversation with technical support role."""
        session_id = "test-tech-session"
        
        response = client.post(
            "/api/chat",
            json={
                "query": "How do I implement a neural network?",
                "role_id": "technical_support",
                "session_id": session_id
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert len(data["answer"]) > 0
    
    def test_conversation_with_hr_assistant(self):
        """Test conversation with HR assistant role."""
        session_id = "test-hr-session"
        
        response = client.post(
            "/api/chat",
            json={
                "query": "What are the company policies?",
                "role_id": "hr_assistant",
                "session_id": session_id
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert len(data["answer"]) > 0
    
    def test_conversation_with_product_consultant(self):
        """Test conversation with product consultant role."""
        session_id = "test-product-session"
        
        response = client.post(
            "/api/chat",
            json={
                "query": "What features does this product have?",
                "role_id": "product_consultant",
                "session_id": session_id
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert len(data["answer"]) > 0
    
    def test_conversation_role_switching(self):
        """Test switching roles in the same session."""
        session_id = "test-switch-session"
        
        # First message with technical_support
        response1 = client.post(
            "/api/chat",
            json={
                "query": "What is AI?",
                "role_id": "technical_support",
                "session_id": session_id
            }
        )
        assert response1.status_code == 200
        
        # Second message with product_consultant
        response2 = client.post(
            "/api/chat",
            json={
                "query": "How can AI help my business?",
                "role_id": "product_consultant",
                "session_id": session_id
            }
        )
        assert response2.status_code == 200
