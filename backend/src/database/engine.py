from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.config.settings import settings
import os

# Create async engine with Neon PostgreSQL connection
# Convert standard PostgreSQL URL to asyncpg-compatible URL by changing postgresql:// to postgresql+asyncpg://
database_url = settings.DATABASE_URL or os.getenv("DATABASE_URL", "")
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
) # Missing closing parenthesis

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
    Initialize database tables
    """
    from sqlmodel import SQLModel
    from sqlalchemy import text
    import logging

    # For development, we'll drop and recreate tables to handle schema changes
    # Need to handle foreign key constraints by dropping in the right order or using CASCADE
    async with engine.begin() as conn:
        # First, drop all foreign key constraints, then drop tables
        # Alternative: Use raw SQL to drop all tables with CASCADE
        try:
            # Drop all tables in the right order or with CASCADE
            # Since SQLModel doesn't handle CASCADE on drop_all, we'll use raw SQL
            await conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
            await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))

            # Now create all tables with the correct schema
            await conn.run_sync(SQLModel.metadata.create_all)
        except Exception as e:
            print(f"Error during initial table drop: {e}")
            # If the above fails, try creating tables directly (might work if they don't exist yet)
            await conn.run_sync(SQLModel.metadata.create_all)

    print("Database tables initialized successfully!")