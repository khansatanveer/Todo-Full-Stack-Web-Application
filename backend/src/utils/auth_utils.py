import bcrypt

def hash_password(password: str) -> str:
    # bcrypt has a 72-byte limit. We truncate manually to avoid ValueError.
    # Note: Modern bcrypt handles this but passlib doesn't and raises ValueError.
    # We use utf-8 encoding and take the first 72 bytes.
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Slicing bytes and then decoding back to string safely
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate to 72 bytes to be safe and match hashing
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # bcrypt.checkpw expects bytes for both arguments
    try:
        return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
    except Exception:
        return False

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