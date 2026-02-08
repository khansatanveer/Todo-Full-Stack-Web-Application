from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from .engine import AsyncSessionLocal

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Generate database sessions for dependency injection.
    Ensures proper cleanup of resources after each request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()