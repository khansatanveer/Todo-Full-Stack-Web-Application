from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db_session
from src.core.auth import get_current_user
from src.services.user_service import UserService
from src.utils.auth_utils import check_cross_user_access_attempt
import uuid

router = APIRouter(tags=["users"])

# Specific route first to avoid matching "/me" as a user_id
@router.get("/me")
async def read_users_me(
    current_user_payload: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get information about the currently authenticated user
    Returns data from JWT token payload (no database lookup needed)
    """
    return {
        "id": str(current_user_payload["user_id"]),
        "email": current_user_payload["email"],
        "name": current_user_payload.get("name") or "",
    }

@router.get("/{user_id}")
async def get_user_by_id(
    user_id: str = Path(..., description="The ID of the user to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific user's information.
    Users can only access their own information.
    """
    # Check if the current user is trying to access their own data
    if check_cross_user_access_attempt(current_user, user_id):
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: You can only access your own user information"
        )

    # Fetch user from database
    user = await UserService.get_user_by_id(db_session, str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
    }


@router.put("/{user_id}")
async def update_user_by_id(
    user_data: Dict[str, Any],
    user_id: str = Path(..., description="The ID of the user to update"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Update a specific user's information.
    Users can only update their own information.
    """
    # Check if the current user is trying to update their own data
    if check_cross_user_access_attempt(current_user, user_id):
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: You can only update your own user information"
        )

    # Fetch and update user
    user = await UserService.get_user_by_id(db_session, str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    if "name" in user_data:
        user.name = user_data["name"]
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "message": f"Successfully updated user {user_id}"
    }


@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: str = Path(..., description="The ID of the user to delete"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific user.
    Users can only delete their own account.
    """
    # Check if the current user is trying to delete their own account
    if check_cross_user_access_attempt(current_user, user_id):
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: You can only delete your own account"
        )

    # Fetch user
    user = await UserService.get_user_by_id(db_session, str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete user
    await db_session.delete(user)
    await db_session.commit()
    
    return {
        "user_id": str(user_id),
        "message": f"Successfully deleted user {user_id} account"
    }
