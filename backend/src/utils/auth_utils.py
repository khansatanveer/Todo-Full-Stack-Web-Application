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
    return str(current_user["user_id"]) != str(target_user_id)