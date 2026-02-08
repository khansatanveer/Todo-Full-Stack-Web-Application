from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .task import Task  # Import for type checking to avoid circular imports


class UserBase(SQLModel):
    """Base class for User model with common fields"""
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    """
    User model representing a registered user with email, authentication credentials, and unique identifier.
    Fields:
    - id (UUID): Unique identifier for the user
    - email (String): User's email address (unique)
    - created_at (DateTime): Timestamp of user creation
    - updated_at (DateTime): Timestamp of last update
    """
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks (one-to-many)
    tasks: List["Task"] = Relationship(back_populates="owner")

    # Validation: Email must be valid format, unique constraint on email
    def __str__(self):
        return f"User(id={self.id}, email={self.email})"