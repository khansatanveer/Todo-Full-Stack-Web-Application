from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
import os

def get_secret_key() -> str:
    """Get the JWT secret key from environment"""
    secret = os.getenv("BETTER_AUTH_SECRET")
    if not secret:
        # Fallback to SECRET_KEY for backward compatibility
        secret = os.getenv("SECRET_KEY")
    if not secret:
        raise ValueError("No JWT secret key configured")
    return secret

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_secret_key(), algorithm="HS256")
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
        return payload
    except JWTError:
        raise credentials_exception