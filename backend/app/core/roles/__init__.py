"""Role configurations for the RAG Knowledge Base API.

This module provides predefined roles that define AI assistant behaviors.
Each role has a unique system prompt that shapes how the assistant responds.
"""

from typing import List, Optional

from app.models.role import Role
from app.core.roles.technical_support import TECHNICAL_SUPPORT_ROLE
from app.core.roles.hr_assistant import HR_ASSISTANT_ROLE
from app.core.roles.product_consultant import PRODUCT_CONSULTANT_ROLE


# List of all predefined roles
PREDEFINED_ROLES: List[Role] = [
    TECHNICAL_SUPPORT_ROLE,
    HR_ASSISTANT_ROLE,
    PRODUCT_CONSULTANT_ROLE,
]


def get_role_by_id(role_id: str) -> Optional[Role]:
    """Retrieve a role configuration by its unique identifier.
    
    Args:
        role_id: The unique identifier of the role to retrieve.
        
    Returns:
        Role: The role configuration if found, None otherwise.
        
    Examples:
        >>> role = get_role_by_id("technical_support")
        >>> if role:
        ...     print(role.name)
        技术支持
    """
    for role in PREDEFINED_ROLES:
        if role.id == role_id:
            return role
    return None


__all__ = [
    "PREDEFINED_ROLES",
    "get_role_by_id",
    "TECHNICAL_SUPPORT_ROLE",
    "HR_ASSISTANT_ROLE",
    "PRODUCT_CONSULTANT_ROLE",
]