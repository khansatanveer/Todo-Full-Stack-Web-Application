from fastapi import Request, HTTPException, Depends
from typing import Dict, Any
import os
from datetime import datetime
import jwt
from jwt import DecodeError, ExpiredSignatureError
from ..models.user import User
import uuid


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
    secret = os.getenv("BETTER_AUTH_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Authentication secret not configured")

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

        # Return the user information
        return {
            "user_id": user_id,
            "email": payload["email"],
            "exp": exp
        }

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token: unable to decode")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token: signature verification failed")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")