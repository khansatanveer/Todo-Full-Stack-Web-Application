import asyncio
import sys
from pathlib import Path

# Add src folder to Python path so we can import modules from src
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

# Import init_db from engine.py
from database.engine import init_db

asyncio.run(init_db())
