"""Tests for Chat API endpoints."""

import pytest
import time
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestChatAPI:
    """Test cases for chat API endpoints."""
    
    def test_chat_endpoint_basic(self):
        """Test basic chat endpoint returns correct format."""
        response = client.post(
            "/api/chat",
            json={
                "query": "What is machine learning?",
                "role_id": "technical_support",
                "session_id": "test-session-123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "answer" in data
        assert "sources" in data
        assert "response_time" in data
        assert "retrieved_count" in data
        
        # Check types
        assert isinstance(data["answer"], str)
        assert isinstance(data["sources"], list)
        assert isinstance(data["response_time"], (int, float))
        assert isinstance(data["retrieved_count"], int)
    
    def test_chat_endpoint_with_role(self):
        """Test chat endpoint with different roles."""
        roles = ["technical_support", "hr_assistant", "product_consultant"]
        
        for role in roles:
            response = client.post(
                "/api/chat",
                json={
                    "query": "What is AI?",
                    "role_id": role,
                    "session_id": f"test-session-{role}"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert len(data["answer"]) > 0
    
    def test_chat_endpoint_invalid_role(self):
        """Test chat endpoint with invalid role returns 404."""
        response = client.post(
            "/api/chat",
            json={
                "query": "What is AI?",
                "role_id": "invalid_role",
                "session_id": "test-session-invalid"
            }
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_chat_endpoint_empty_question(self):
        """Test chat endpoint with empty question returns validation error."""
        response = client.post(
            "/api/chat",
            json={
                "query": "",
                "role_id": "technical_support",
                "session_id": "test-session-empty"
            }
        )
        
        # Should return 422 validation error
        assert response.status_code == 422
    
    def test_chat_response_time(self):
        """Test chat response time is under 5 seconds."""
        start_time = time.time()
        
        response = client.post(
            "/api/chat",
            json={
                "query": "What is machine learning?",
                "role_id": "technical_support",
                "session_id": "test-session-time"
            }
        )
        
        elapsed_time = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed_time < 5.0, f"Response took {elapsed_time:.2f}s, expected < 5s"
    
    def test_chat_citations_format(self):
        """Test that citations are properly formatted."""
        response = client.post(
            "/api/chat",
            json={
                "query": "What is AI?",
                "role_id": "technical_support",
                "session_id": "test-session-citations"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check citation structure
        for source in data["sources"]:
            assert "document_id" in source
            assert "chunk_index" in source
            assert "content_preview" in source
            assert "score" in source
            
            assert isinstance(source["document_id"], str)
            assert isinstance(source["chunk_index"], int)
            assert isinstance(source["content_preview"], str)
            assert isinstance(source["score"], float)
            assert 0.0 <= source["score"] <= 1.0


class TestChatHistoryAPI:
    """Test cases for chat history API endpoints."""
    
    def test_get_chat_history_endpoint(self):
        """Test GET /api/chat/history/{session_id} endpoint."""
        response = client.get("/api/chat/history/test-session-123")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "session_id" in data
        assert "messages" in data
        assert "total" in data
        assert isinstance(data["messages"], list)
    
    def test_chat_history_pagination(self):
        """Test chat history pagination."""
        response = client.get("/api/chat/history/test-session-123?limit=10")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "messages" in data
        assert len(data["messages"]) <= 10


class TestFeedbackAPI:
    """Test cases for feedback API endpoints."""
    
    def test_submit_feedback_thumbs_up(self):
        """Test submitting thumbs up feedback."""
        response = client.post(
            "/api/chat/feedback",
            params={
                "message_id": "msg-123",
                "feedback_type": "thumbs_up"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_submit_feedback_thumbs_down(self):
        """Test submitting thumbs down feedback."""
        response = client.post(
            "/api/chat/feedback",
            params={
                "message_id": "msg-456",
                "feedback_type": "thumbs_down",
                "comment": "Not helpful"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_submit_feedback_invalid_type(self):
        """Test submitting invalid feedback type returns 400."""
        response = client.post(
            "/api/chat/feedback",
            params={
                "message_id": "msg-789",
                "feedback_type": "invalid_type"
            }
        )
        
        assert response.status_code == 400
