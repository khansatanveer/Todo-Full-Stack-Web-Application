from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.config.settings import settings
import os

# Determine the database URL based on the environment
database_url = settings.DATABASE_URL or os.getenv("DATABASE_URL", "")

# Check if it's a SQLite URL
if database_url.startswith("sqlite://"):
    # Use sqlite for local development
    engine = create_async_engine(
        database_url,
        echo=False,
        connect_args={"check_same_thread": False}  # Required for SQLite
    )
else:
    # Use PostgreSQL for production
    # Convert standard PostgreSQL URL to asyncpg-compatible URL by changing postgresql:// to postgresql+asyncpg://
    if database_url and database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        # Remove sslmode and channel_binding from URL string if present, handle via connect_args
        if "?" in database_url:
            database_url = database_url.split("?")[0]

    engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={"ssl": True} # Explicitly enable SSL
    )

# Create async session factory
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def get_db_session():
    """
    Dependency to get database session
    """
    async with AsyncSessionLocal() as session:
        yield session

# Function to initialize the database tables
async def init_db():
    """
    Initialize database tables (only create, don't drop)
    """
    from sqlmodel import SQLModel
    from sqlalchemy import text
    import logging

    try:
        async with engine.begin() as conn:
            # Only create tables, don't drop existing ones
            await conn.run_sync(SQLModel.metadata.create_all)
        print("Database tables initialized successfully!")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise


    