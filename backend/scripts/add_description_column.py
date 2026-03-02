"""
Migration script to add description column to tasks table
"""
import asyncio
from sqlalchemy import text, inspect
from src.database.engine import engine, AsyncSessionLocal
from sqlmodel import SQLModel


async def add_description_column():
    """Add description column to tasks table if it doesn't exist"""
    
    async with engine.begin() as conn:
        # Check if column exists
        inspector = await conn.run_sync(lambda sync_conn: inspect(sync_conn))
        
        # Get table columns
        columns = [col['name'] for col in await conn.run_sync(lambda sync_conn: inspector.get_columns('tasks'))]
        
        if 'description' not in columns:
            print("Adding 'description' column to tasks table...")
            await conn.execute(text(
                "ALTER TABLE tasks ADD COLUMN description VARCHAR;"
            ))
            print("Successfully added 'description' column!")
        else:
            print("'description' column already exists.")


if __name__ == "__main__":
    asyncio.run(add_description_column())
