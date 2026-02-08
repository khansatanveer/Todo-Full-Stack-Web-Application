from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    # Inherits all fields from TaskBase
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskPublic(TaskBase):
    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    tasks: list[TaskPublic]
    total_count: int
    completed_count: int
    incomplete_count: int