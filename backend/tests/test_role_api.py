"""Tests for Role API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestRoleAPI:
    """Test cases for role API endpoints."""
    
    def test_list_roles(self):
        """Test GET /api/roles returns all predefined roles."""
        response = client.get("/api/roles")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "roles" in data
        assert "total" in data
        
        # Check we have 3 predefined roles
        assert data["total"] == 3
        assert len(data["roles"]) == 3
        
        # Check role IDs
        role_ids = [role["id"] for role in data["roles"]]
        assert "technical_support" in role_ids
        assert "hr_assistant" in role_ids
        assert "product_consultant" in role_ids
    
    def test_get_role_technical_support(self):
        """Test getting technical support role details."""
        response = client.get("/api/roles/technical_support")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "technical_support"
        assert data["name"] == "技术支持"
        assert "description" in data
        assert "system_prompt" in data
        assert "icon" in data
    
    def test_get_role_hr_assistant(self):
        """Test getting HR assistant role details."""
        response = client.get("/api/roles/hr_assistant")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "hr_assistant"
        assert data["name"] == "HR 助手"
        assert "description" in data
        assert "system_prompt" in data
    
    def test_get_role_product_consultant(self):
        """Test getting product consultant role details."""
        response = client.get("/api/roles/product_consultant")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == "product_consultant"
        assert data["name"] == "产品顾问"
        assert "description" in data
        assert "system_prompt" in data
    
    def test_get_role_not_found(self):
        """Test getting non-existent role returns 404."""
        response = client.get("/api/roles/nonexistent_role")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_role_schema(self):
        """Test that role schema has all required fields."""
        response = client.get("/api/roles")
        
        assert response.status_code == 200
        data = response.json()
        
        for role in data["roles"]:
            # Check all required fields exist
            assert "id" in role
            assert "name" in role
            assert "description" in role
            assert "system_prompt" in role
            
            # Check types
            assert isinstance(role["id"], str)
            assert isinstance(role["name"], str)
            assert isinstance(role["description"], str)
            assert isinstance(role["system_prompt"], str)
            
            # Check values are not empty
            assert len(role["id"]) > 0
            assert len(role["name"]) > 0
            assert len(role["description"]) > 0
            assert len(role["system_prompt"]) > 10
    
    def test_default_role(self):
        """Test that technical_support is the default role."""
        response = client.get("/api/roles/technical_support")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["is_default"] is True
