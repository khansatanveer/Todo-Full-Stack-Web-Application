from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Import models to ensure SQLModel metadata is aware of them
from src.models import user, task

# Import routes
from src.api import task_routes
from src.api.routes import auth as auth_routes
from src.api.routes import users as users_routes
from src.database.engine import init_db


# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init_db()
    print("Database initialized.")
    yield


# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="Secure Todo API with JWT authentication and user-scoped tasks",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://khansatanveer-full-stack-todo.hf.space",
        "https://todo-full-stack-web-application-three.vercel.app",
        "https://todo-full-stack-web-application-khansas-projects-79799e71.vercel.app",
        "https://todo-full-stack-web-applic-git-de8d8f-khansas-projects-79799e71.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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