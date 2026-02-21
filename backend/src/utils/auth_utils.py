from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def check_cross_user_access_attempt(current_user: dict, target_user_id: str) -> bool:
    """
    Checks if the current user is attempting to access or modify data
    that does not belong to them.
    """
    # Handle both dict and User object formats
    if hasattr(current_user, 'id'):
        # If current_user is a User object, access its id attribute
        current_user_id = str(current_user.id)
    else:
        # If current_user is a dict, access user_id key
        current_user_id = str(current_user.get("user_id", current_user.get("id", "")))

    return current_user_id != str(target_user_id)