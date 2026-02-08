from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from .user import User  # Import User for the relationship


class TaskBase(SQLModel):
    """Base class for Task model with common fields"""
    title: str = Field(min_length=1, max_length=255)
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)  # Foreign key linking to User


class Task(TaskBase, table=True):
    """
    Task model representing a todo item that belongs to a specific user, containing title,
    description, completion status, and creation timestamp.
    Fields:
    - id (UUID): Unique identifier for the task
    - title (String): Task title/description
    - completed (Boolean): Whether the task is completed
    - user_id (UUID): Foreign key linking to User
    - created_at (DateTime): Timestamp of task creation
    - updated_at (DateTime): Timestamp of last update
    """
    __tablename__ = "tasks"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user (many-to-one)
    owner: Optional["User"] = Relationship(back_populates="tasks", sa_relationship_kwargs={"lazy": "select"})


class TaskPublic(TaskBase):
    """
    Public representation of Task without internal fields
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime