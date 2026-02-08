"""
Authentication Configuration
"""
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AuthConfig:
    """Authentication configuration settings"""

    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("BETTER_AUTH_SECRET", "")
    if not JWT_SECRET_KEY:
        raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour

    # Token validation settings
    VERIFY_SIGNATURE: bool = True
    VERIFY_EXP: bool = True
    VERIFY_IAT: bool = True
    VERIFY_NBF: bool = False
    VERIFY_SUB: True
    VERIFY_AUD: False
    VERIFY_ISS: False

    @classmethod
    def validate_config(cls):
        """Validate the configuration settings"""
        if not cls.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY must be set")

        if len(cls.JWT_SECRET_KEY) < 32:
            print("Warning: JWT_SECRET_KEY should be at least 32 characters long for security")

        return True