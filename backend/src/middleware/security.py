from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
import logging
import re

# Configure logger
logger = logging.getLogger(__name__)

class SecurityMiddleware:
    """
    Security middleware to handle various security concerns
    """

    def __init__(self):
        self.blocked_patterns = [
            r'<script[^>]*>',  # XSS prevention
            r'javascript:',     # JavaScript protocol
            r'on\w+\s*=',      # Event handlers
            r'eval\s*\(',      # eval function
            r'expression\s*\(', # CSS expressions
        ]

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable]):
        # Sanitize request data to prevent injection attacks
        request = await self.sanitize_request(request)

        try:
            response = await call_next(request)

            # Add security headers to response
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

            return response
        except HTTPException as e:
            # Sanitize error details to prevent information disclosure
            sanitized_detail = self.sanitize_error_detail(str(e.detail))
            logger.warning(f"HTTP Exception caught and sanitized: {e.status_code}")

            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": "REQUEST_ERROR",
                    "message": sanitized_detail,
                    "status_code": e.status_code
                }
            )
        except Exception as e:
            # Log the actual error for debugging (server-side only)
            logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)

            # Return generic error to prevent information disclosure
            return JSONResponse(
                status_code=500,
                content={
                    "error": "INTERNAL_ERROR",
                    "message": "An internal error occurred",
                    "status_code": 500
                }
            )

    async def sanitize_request(self, request: Request):
        """
        Sanitize incoming request to prevent injection attacks
        """
        # For now, just return the request as-is
        # In a more complete implementation, we'd sanitize body, query params, etc.
        return request

    def sanitize_error_detail(self, detail: str) -> str:
        """
        Sanitize error details to prevent information disclosure
        """
        if not detail:
            return "An error occurred"

        # Remove potential sensitive information from error details
        sanitized = detail

        # Replace any database-related errors
        if 'database' in detail.lower() or 'connection' in detail.lower():
            sanitized = "Service temporarily unavailable"
        elif 'file' in detail.lower() or 'path' in detail.lower():
            sanitized = "Request could not be processed"
        elif 'traceback' in detail.lower() or 'stack' in detail.lower():
            sanitized = "Internal server error occurred"
        elif 'secret' in detail.lower() or 'key' in detail.lower():
            sanitized = "Authentication error occurred"
        elif 'password' in detail.lower():
            sanitized = "Authentication failed"

        # Remove potential SQL injection indicators
        sql_indicators = ['select', 'union', 'drop', 'delete', 'update', 'insert']
        detail_lower = detail.lower()
        for indicator in sql_indicators:
            if indicator in detail_lower:
                sanitized = "Request validation failed"
                break

        return sanitized


def get_security_middleware():
    """
    Factory function to get security middleware instance
    """
    return SecurityMiddleware()