"""Role models for AI assistant configuration in the RAG Knowledge Base API."""

import re
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class RoleBase(BaseModel):
    """Base model for role configuration.
    
    Attributes:
        id: Unique role identifier (alphanumeric and underscore only).
        name: Display name for the role (2-50 characters).
        description: Brief description of the role's purpose.
        system_prompt: System prompt that defines the role's behavior.
        icon: Optional icon (emoji or URL) for the role.
        is_default: Whether this is the default role.
    """
    
    id: str = Field(
        ...,
        description="Unique role identifier",
        examples=["technical_support", "hr_assistant", "product_consultant"]
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Display name for the role",
        examples=["技术支持", "HR 助手", "产品顾问"]
    )
    description: str = Field(
        ...,
        description="Brief description of the role's purpose",
        examples=["专门解答技术问题，提供详细的解决方案"]
    )
    system_prompt: str = Field(
        ...,
        min_length=10,
        description="System prompt that defines the role's behavior"
    )
    icon: Optional[str] = Field(
        default=None,
        description="Optional icon (emoji or URL) for the role",
        examples=["🔧", "👤", "💼"]
    )
    is_default: bool = Field(
        default=False,
        description="Whether this is the default role"
    )
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate that id contains only alphanumeric characters and underscores.
        
        Args:
            v: Role ID string.
            
        Returns:
            str: Validated role ID.
            
        Raises:
            ValueError: If ID contains invalid characters.
        """
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Role ID must contain only alphanumeric characters and underscores')
        return v
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "id": "technical_support",
                "name": "技术支持",
                "description": "专门解答技术问题，提供详细的解决方案",
                "system_prompt": "你是一位专业的技术支持助手...",
                "icon": "🔧",
                "is_default": True
            }
        }


class Role(RoleBase):
    """Complete role model with timestamps.
    
    Extends RoleBase with system-generated timestamp fields.
    Used for storing and retrieving role configurations.
    
    Attributes:
        created_at: Timestamp when the role was created.
        updated_at: Timestamp when the role was last updated.
    """
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the role was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the role was last updated"
    )
    
    class Config:
        """Pydantic model configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "technical_support",
                "name": "技术支持",
                "description": "专门解答技术问题，提供详细的解决方案",
                "system_prompt": "你是一位专业的技术支持助手...",
                "icon": "🔧",
                "is_default": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


class RoleListResponse(BaseModel):
    """Model for role listing endpoint responses.
    
    Contains a list of roles and total count for pagination support.
    Used in GET /api/roles response.
    
    Attributes:
        roles: List of role configurations.
        total: Total number of roles.
    """
    
    roles: List[Role] = Field(
        default=[],
        description="List of role configurations"
    )
    total: int = Field(
        ...,
        ge=0,
        description="Total number of roles"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "roles": [
                    {
                        "id": "technical_support",
                        "name": "技术支持",
                        "description": "专门解答技术问题，提供详细的解决方案",
                        "system_prompt": "你是一位专业的技术支持助手...",
                        "icon": "🔧",
                        "is_default": True,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                ],
                "total": 1
            }
        }