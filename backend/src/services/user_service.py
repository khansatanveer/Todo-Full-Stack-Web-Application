from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user import User
from src.schemas.user import UserCreate
from src.utils.auth_utils import hash_password, verify_password
from datetime import datetime


class UserService:
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate):
        # Hash the password before storing
        hashed_password = hash_password(user.password)

        # Create the user instance with all required fields
        db_user = User(
            email=user.email,
            name=user.name,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str):
        # Get user by email
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return None

        # Verify the password
        if not verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    async def update_timestamp(db: AsyncSession, user: User):
        """Update the updated_at timestamp for a user"""
        user.updated_at = datetime.utcnow()
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user