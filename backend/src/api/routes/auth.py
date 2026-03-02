from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_db_session
from src.schemas.user import UserCreate, UserLogin
from src.services.user_service import UserService
from src.utils.jwt_utils import create_access_token
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])

# --- HELPERS ---
def generate_auth_response(user):
    """Token generate karne ka common logic"""
    # Include user ID, email, and name in JWT token
    access_token = create_access_token(data={
        "sub": str(user.id),  # User ID as subject
        "email": user.email,
        "name": user.name
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }

# --- ENDPOINTS ---

@router.post("/sign-up/email")
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    try:
        new_user = await UserService.create_user(db, user=user)
        return generate_auth_response(new_user)
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed.",
        )

# 1. Yeh Frontend ke liye hai (Jo JSON accept karta hai)
@router.post("/sign-in/email")
async def login_user_frontend(user_credentials: UserLogin, db: AsyncSession = Depends(get_db_session)):
    db_user = await UserService.authenticate_user(
        db,
        email=user_credentials.email,
        password=user_credentials.password
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return generate_auth_response(db_user)

# 2. Yeh Swagger 'Authorize' button ke liye hai (Jo Form-Data accept karta hai)
# Iska path '/login' rakha hai taaki hum tokenUrl se match kar sakein
@router.post("/login")
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db_session)
):
    # Note: Swagger email ko 'username' field mein bhejta hai
    db_user = await UserService.authenticate_user(
        db,
        email=form_data.username, 
        password=form_data.password
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return generate_auth_response(db_user)