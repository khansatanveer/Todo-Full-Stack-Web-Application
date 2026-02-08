from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
import logging

# Configure logger
logger = logging.getLogger(__name__)

class AuthException(HTTPException):
    """Custom exception for authentication-related errors"""

    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(status_code=status_code, detail=detail)
        logger.warning(f"AuthException: {detail}")


class AuthorizationException(HTTPException):
    """Custom exception for authorization-related errors"""

    def __init__(self, detail: str, status_code: int = status.HTTP_403_FORBIDDEN):
        super().__init__(status_code=status_code, detail=detail)
        logger.warning(f"AuthorizationException: {detail}")


def create_error_response(error_code: str, message: str, status_code: int = 400):
    """
    Create a consistent error response format
    """
    return {
        "error": error_code,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": status_code
    }


def handle_auth_error(error_msg: str, request_details: Optional[dict] = None):
    """
    Standardized authentication error handling
    """
    # Log the error for monitoring (without sensitive information)
    logger.info(f"Authentication error: {error_msg}")

    if request_details:
        # Log non-sensitive request details for debugging
        logger.debug(f"Request details: {request_details.get('path', '')} {request_details.get('method', '')}")

    # Return generic error response to prevent information leakage
    return create_error_response(
        error_code="UNAUTHORIZED_ACCESS",
        message="Unauthorized access",
        status_code=401
    )


def handle_authorization_error(error_msg: str, request_details: Optional[dict] = None):
    """
    Standardized authorization error handling
    """
    # Log the error for monitoring (without sensitive information)
    logger.info(f"Authorization error: {error_msg}")

    if request_details:
        # Log non-sensitive request details for debugging
        logger.debug(f"Authorization request details: {request_details.get('path', '')} {request_details.get('method', '')}")

    # Return generic error response to prevent information leakage
    return create_error_response(
        error_code="FORBIDDEN_ACCESS",
        message="Forbidden access",
        status_code=403
    )


def sanitize_error_message(error: Exception) -> str:
    """
    Sanitize error messages to prevent information leakage
    """
    error_str = str(error)

    # Remove potentially sensitive information from error messages
    sanitized = error_str

    # Replace any potential secrets or internal details
    if "secret" in error_str.lower():
        sanitized = "Security-related error occurred"
    elif "database" in error_str.lower() or "connection" in error_str.lower():
        sanitized = "Service temporarily unavailable"
    elif "traceback" in error_str.lower() or "stack" in error_str.lower():
        sanitized = "Internal server error occurred"
    elif "file" in error_str.lower() or "path" in error_str.lower():
        sanitized = "Request could not be processed"

    return sanitized