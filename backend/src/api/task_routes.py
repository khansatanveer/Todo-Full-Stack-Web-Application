from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from src.models.task import Task, TaskPublic
from src.schemas.task import TaskCreate, TaskUpdate, TaskListResponse
from src.core.auth import get_current_user
from src.database.session import get_db_session
from src.services.task_service import (
    create_task,
    get_tasks_by_user,
    get_task_by_id_and_user,
    update_task_by_id_and_user,
    delete_task_by_id_and_user,
    toggle_task_completion
)

router = APIRouter(prefix="/api", tags=["tasks"])

# -------------------------------
# List all tasks for the authenticated user
# -------------------------------
@router.get("/tasks", response_model=TaskListResponse)
async def list_tasks(
    current_user: dict = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve all tasks for the authenticated user.
    Filters tasks by the user_id from the JWT token.
    """
    user_id = current_user["user_id"]

    tasks = await get_tasks_by_user(db_session, str(user_id))

    total_count = len(tasks)
    completed_count = sum(1 for task in tasks if task.completed)
    incomplete_count = total_count - completed_count

    return TaskListResponse(
        tasks=tasks,
        total_count=total_count,
        completed_count=completed_count,
        incomplete_count=incomplete_count
    )

# -------------------------------
# Create a new task for the authenticated user
# -------------------------------
@router.post("/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_create: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Create a new task for the authenticated user.
    Assigns the task to the user_id from the JWT token.
    """
    user_id = current_user["user_id"]

    task = await create_task(db_session, task_create, str(user_id))
    return task

# -------------------------------
# Get a single task by ID
# -------------------------------
@router.get("/tasks/{task_id}", response_model=TaskPublic)
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve a specific task by ID for the authenticated user.
    Verifies that the task belongs to the authenticated user.
    """
    user_id = current_user["user_id"]

    # Verify the task_id is a valid UUID
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = await get_task_by_id_and_user(db_session, task_id, str(user_id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to authenticated user"
        )

    return task

# -------------------------------
# Update a task
# -------------------------------
@router.put("/tasks/{task_id}", response_model=TaskPublic)
async def update_existing_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Update a specific task for the authenticated user.
    Verifies that the task belongs to the authenticated user before updating.
    """
    user_id = current_user["user_id"]

    # Verify the task_id is a valid UUID
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = await update_task_by_id_and_user(db_session, task_id, str(user_id), task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to authenticated user"
        )

    return task

# -------------------------------
# Delete a task
# -------------------------------
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific task for the authenticated user.
    Verifies that the task belongs to the authenticated user before deletion.
    """
    user_id = current_user["user_id"]

    # Verify the task_id is a valid UUID
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    success = await delete_task_by_id_and_user(db_session, task_id, str(user_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to authenticated user"
        )

    return

# -------------------------------
# Toggle task completion
# -------------------------------
@router.patch("/tasks/{task_id}/complete", response_model=TaskPublic)
async def toggle_task_complete(
    task_id: str,
    current_user: dict = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user.
    Verifies that the task belongs to the authenticated user before toggling.
    """
    user_id = current_user["user_id"]

    # Verify the task_id is a valid UUID
    try:
        uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    task = await toggle_task_completion(db_session, task_id, str(user_id))
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to authenticated user"
        )

    return task