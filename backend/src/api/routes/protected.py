from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from src.api.deps import get_current_active_user

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/profile")
def get_user_profile(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """
    Protected endpoint to get user profile information
    Requires valid JWT token
    """
    return {
        "user_id": current_user["user_id"],
        "email": current_user["user_email"],
        "message": "Profile accessed successfully"
    }


@router.get("/data")
def get_user_data(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """
    Protected endpoint to get user-specific data
    Requires valid JWT token
    """
    return {
        "user_id": current_user["user_id"],
        "data": f"Personal data for user {current_user['user_email']}",
        "message": "User data accessed successfully"
    }


@router.post("/action")
def perform_user_action(
    action_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Protected endpoint to perform an action on behalf of the user
    Requires valid JWT token
    """
    return {
        "user_id": current_user["user_id"],
        "action": action_data.get("action", "unknown"),
        "message": "Action performed successfully"
    }