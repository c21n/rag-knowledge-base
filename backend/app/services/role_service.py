"""Role management service for the RAG Knowledge Base API.

This module provides business logic for role operations including:
- Listing all available roles
- Retrieving roles by ID
- Getting the default role
- Validating role existence
"""

import logging
from typing import List, Optional

from app.models.role import Role
from app.core.roles import PREDEFINED_ROLES, get_role_by_id as get_predefined_role

logger = logging.getLogger(__name__)


class RoleService:
    """Service class for role management operations.
    
    Handles all business logic related to role configuration retrieval
    and validation. Manages role caching for performance.
    
    This service loads predefined roles from the roles module and provides
    a clean interface for the RAG service to access role-specific system prompts.
    
    Attributes:
        _roles: Cached list of role configurations.
        _roles_by_id: Dictionary mapping role IDs to roles for fast lookup.
    """
    
    def __init__(self):
        """Initialize RoleService with predefined roles.
        
        Loads all predefined roles and builds lookup structures for
        efficient retrieval.
        """
        self._roles: List[Role] = PREDEFINED_ROLES.copy()
        self._roles_by_id: dict = {role.id: role for role in self._roles}
        logger.info(f"RoleService initialized with {len(self._roles)} roles")
    
    def list_roles(self) -> List[Role]:
        """List all available roles.
        
        Returns a copy of the predefined roles list to prevent
        modification of the internal state.
        
        Returns:
            List[Role]: List of all available role configurations.
        """
        logger.debug(f"Listing {len(self._roles)} roles")
        return self._roles.copy()
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """Retrieve a role by its unique identifier.
        
        Args:
            role_id: The unique identifier of the role to retrieve.
            
        Returns:
            Role: The role configuration if found, None otherwise.
            
        Examples:
            >>> service = RoleService()
            >>> role = service.get_role("technical_support")
            >>> if role:
            ...     print(role.name)
            技术支持
        """
        role = self._roles_by_id.get(role_id)
        if role:
            logger.debug(f"Retrieved role: {role_id}")
        else:
            logger.warning(f"Role not found: {role_id}")
        return role
    
    def get_default_role(self) -> Role:
        """Get the default role for the system.
        
        Returns the technical support role as the default. This role is
        used when no specific role is specified by the user.
        
        Returns:
            Role: The default role (technical support).
            
        Raises:
            ValueError: If no default role is configured.
        """
        # Look for the role marked as default
        for role in self._roles:
            if role.is_default:
                logger.debug(f"Default role: {role.id}")
                return role
        
        # Fallback to technical_support if no default is marked
        default_role = self.get_role("technical_support")
        if default_role:
            return default_role
        
        # This should never happen if roles are properly configured
        raise ValueError("No default role configured and technical_support role not found")
    
    def validate_role(self, role_id: str) -> bool:
        """Validate that a role ID exists in the system.
        
        Args:
            role_id: The role identifier to validate.
            
        Returns:
            bool: True if the role exists, False otherwise.
            
        Examples:
            >>> service = RoleService()
            >>> service.validate_role("technical_support")
            True
            >>> service.validate_role("invalid_role")
            False
        """
        is_valid = role_id in self._roles_by_id
        logger.debug(f"Role validation for '{role_id}': {is_valid}")
        return is_valid


# Singleton instance
_role_service_instance: Optional[RoleService] = None


def get_role_service() -> RoleService:
    """Get the singleton instance of RoleService.
    
    Creates a new instance on first call and returns the same instance
    on subsequent calls for efficient resource usage.
    
    Returns:
        RoleService: The singleton RoleService instance.
        
    Examples:
        >>> service = get_role_service()
        >>> roles = service.list_roles()
        >>> print(len(roles))
        3
    """
    global _role_service_instance
    if _role_service_instance is None:
        _role_service_instance = RoleService()
    return _role_service_instance


__all__ = ["RoleService", "get_role_service"]