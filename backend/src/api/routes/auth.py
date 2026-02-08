from fastapi import APIRouter, Depends, HTTPException, status
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
        access_token = create_access_token(data={"sub": new_user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to an unexpected error. Please try again later.",
        )


@router.post("/sign-in/email")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db_session)):
    db_user = await UserService.authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}