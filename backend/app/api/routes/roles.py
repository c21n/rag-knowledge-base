"""
Role API routes for role management.
"""
import logging
from fastapi import APIRouter, HTTPException
from typing import List

from app.services.role_service import get_role_service
from app.models.role import RoleListResponse

logger = logging.getLogger(__name__)

router = APIRouter()
role_service = get_role_service()


@router.get("/api/roles", response_model=RoleListResponse)
async def list_roles():
    """
    List all available roles.
    
    Returns:
        RoleListResponse with all predefined roles.
    """
    roles = role_service.list_roles()
    return RoleListResponse(roles=roles, total=len(roles))


@router.get("/api/roles/{role_id}")
async def get_role(role_id: str):
    """
    Get a specific role by ID.
    
    Args:
        role_id: Role identifier.
        
    Returns:
        Role details.
        
    Raises:
        HTTPException: If role not found.
    """
    role = role_service.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found")
    return role
