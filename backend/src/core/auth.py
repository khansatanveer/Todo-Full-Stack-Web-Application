from fastapi import Request, HTTPException, Depends
from typing import Dict, Any
import os
from datetime import datetime
from jose import jwt, JWTError, ExpiredSignatureError
from ..models.user import User
import uuid


def get_secret_key() -> str:
    """Get the JWT secret key from environment"""
    secret = os.getenv("BETTER_AUTH_SECRET")
    if not secret:
        # Fallback to SECRET_KEY for backward compatibility
        secret = os.getenv("SECRET_KEY")
    if not secret:
        raise HTTPException(status_code=500, detail="Authentication secret not configured")
    return secret


def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Extracts and verifies JWT token from Authorization header using BETTER_AUTH_SECRET.
    Returns the user payload (user_id, email, etc.) from the JWT token.

    Args:
        request: The incoming request object containing the Authorization header

    Returns:
        Dict containing user information extracted from JWT payload

    Raises:
        HTTPException: 401 Unauthorized if JWT missing, invalid, or expired
    """
    # Extract Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    # Extract token from "Bearer <token>" format
    token = auth_header.split(" ")[1]

    if not token:
        raise HTTPException(status_code=401, detail="Token not found in Authorization header")

    # Get the secret from environment variables
    secret = get_secret_key()

    try:
        # Verify JWT signature and decode payload
        payload = jwt.decode(token, secret, algorithms=["HS256"])

        # Validate required fields in payload
        if "sub" not in payload or "email" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token: missing required claims")

        # Validate user_id format
        try:
            user_id = uuid.UUID(payload["sub"])
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid token: user ID is not a valid UUID")

        # Check if token is expired
        exp = payload.get("exp")
        if exp:
            if datetime.fromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token has expired")

        # Return the user information - include ALL fields from payload
        return {
            "user_id": user_id,
            "email": payload["email"],
            "name": payload.get("name", ""),
        }

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")