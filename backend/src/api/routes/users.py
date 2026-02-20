from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_active_user
from src.database.session import get_db_session
from src.utils.auth_utils import check_cross_user_access_attempt
from src.services.user_service import UserService
from src.models.user import User
from src.api.deps import get_current_active_user
router = APIRouter(tags=["users"])

@router.get("/{user_id}")
async def get_user_by_id(
    user_id: str = Path(..., description="The ID of the user to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Get a specific user's information.
    Users can only access their own information.
    """
    # Check if the current user is trying to access their own data
    if check_cross_user_access_attempt(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only access your own user information"
        )
    
    # In a real implementation, you would fetch the user from the database
    # For now, we return the current user's info if access is allowed
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "message": f"Successfully retrieved user {user_id} information"
    }


@router.put("/{user_id}")
async def update_user_by_id(
    user_data: Dict[str, Any],
    user_id: str = Path(..., description="The ID of the user to update"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Update a specific user's information.
    Users can only update their own information.
    """
    # Check if the current user is trying to update their own data
    if check_cross_user_access_attempt(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only update your own user information"
        )

    # In a real implementation, you would update the user in the database
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "updated_fields": list(user_data.keys()),
        "message": f"Successfully updated user {user_id} information"
    }


@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: str = Path(..., description="The ID of the user to delete"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific user.
    Users can only delete their own account.
    """
    # Check if the current user is trying to delete their own account
    if check_cross_user_access_attempt(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only delete your own account"
        )

    # In a real implementation, you would delete the user from the database
    return {
        "user_id": current_user.id,
        "message": f"Successfully deleted user {user_id} account"
    }


@router.get("/me")
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get information about the currently authenticated user
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        # Add any other fields you want to expose
        "is_active": current_user.is_active,
    }
