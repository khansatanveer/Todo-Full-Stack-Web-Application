import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.utils.jwt_utils import create_access_token

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_protected_route_without_auth():
    """Test that protected routes return 401 without authentication"""
    response = client.get("/protected/profile")
    assert response.status_code == 401  # Unauthorized


def test_protected_route_with_valid_token():
    """Test that protected routes work with valid authentication token"""
    # Create a valid token for testing
    user_data = {
        "sub": "test_user_id",
        "email": "test@example.com",
        "user_id": "test_user_id"
    }
    token = create_access_token(data=user_data)

    # Make request with valid token
    response = client.get(
        "/protected/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == "test_user_id"
    assert data["email"] == "test@example.com"


def test_user_specific_access_control():
    """Test that users can only access their own data"""
    # Create a token for test user
    user_data = {
        "sub": "user_123",
        "email": "user1@example.com",
        "user_id": "user_123"
    }
    token = create_access_token(data=user_data)

    # Try to access another user's data (should fail)
    response = client.get(
        "/users/user_456",  # Different user ID
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  # Forbidden


def test_user_own_data_access():
    """Test that users can access their own data"""
    # Create a token for test user
    user_data = {
        "sub": "user_123",
        "email": "user1@example.com",
        "user_id": "user_123"
    }
    token = create_access_token(data=user_data)

    # Try to access own data (should succeed)
    response = client.get(
        "/users/user_123",  # Same user ID
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == "user_123"
    assert data["email"] == "user1@example.com"