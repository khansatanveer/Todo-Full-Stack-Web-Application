from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager # Import asynccontextmanager

# Load environment variables
load_dotenv()

# Import and include API routes
from src.api import task_routes
from src.api.routes import auth as auth_routes
from src.api.routes import users as users_routes
from src.database.engine import init_db
from sqlmodel import SQLModel

# Ensure models are imported so SQLModel.metadata is aware of them
from src.models import user, task # Explicitly import models


# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init_db() # Call init_db here
    print("Database initialized.")
    yield


# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="Secure Todo API with JWT authentication and user-scoped tasks",
    version="1.0.0",
    lifespan=lifespan # Pass lifespan to FastAPI app
)

origins = [
    "http://localhost:3000",      # Next.js dev server
    "http://127.0.0.1:3000",      # sometimes needed
    # Add your production frontend domain later, e.g. "https://your-app.vercel.app"
]

# Configure CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # ← no wildcard when credentials=True
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routes
from src.api import task_routes
from src.api.routes import auth as auth_routes
from src.api.routes import users as users_routes
from src.database.engine import engine
from sqlmodel import SQLModel



app.include_router(task_routes.router, prefix="/api", tags=["tasks"])
app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(users_routes.router, prefix="/api/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)