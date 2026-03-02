from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.config.settings import settings
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Get database URL
database_url = settings.DATABASE_URL or os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not set")

# -------------------------
# PostgreSQL Handling
# -------------------------
if database_url.startswith("postgresql://"):

    # Parse the URL
    parsed = urlparse(database_url)
    query_params = parse_qs(parsed.query)

    # Remove unsupported parameters for asyncpg
    query_params.pop("sslmode", None)
    query_params.pop("channel_binding", None)

    # Rebuild query string safely
    new_query = urlencode(query_params, doseq=True)

    # Replace scheme and rebuild full URL
    parsed = parsed._replace(
        scheme="postgresql+asyncpg",
        query=new_query
    )

    database_url = urlunparse(parsed)

# -------------------------
# SQLite Handling
# -------------------------
if database_url.startswith("sqlite:///"):
    database_url = database_url.replace(
        "sqlite:///",
        "sqlite+aiosqlite:///",
        1
    )

# -------------------------
# Engine Creation
# -------------------------
if database_url.startswith("sqlite+aiosqlite"):
    engine = create_async_engine(
        database_url,
        echo=False,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={"ssl": True}  # Enable SSL for asyncpg
    )

# -------------------------
# Session Factory
# -------------------------
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("Database tables initialized successfully!")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise