from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.task import Task, TaskPublic
from src.schemas.task import TaskCreate, TaskUpdate
from datetime import datetime
import uuid


async def create_task(db_session: AsyncSession, task_create: TaskCreate, user_id: str) -> TaskPublic:
    """
    Create a new task with the authenticated user's ID
    """
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=user_id
    )

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    return TaskPublic.from_orm(task)


async def get_tasks_by_user(db_session: AsyncSession, user_id: str) -> List[TaskPublic]:
    """
    Get all tasks for a specific user
    """
    result = await db_session.execute(
        select(Task).where(Task.user_id == user_id)
    )
    tasks = result.scalars().all()

    return [TaskPublic.from_orm(task) for task in tasks]


async def get_task_by_id_and_user(db_session: AsyncSession, task_id: str, user_id: str) -> Optional[TaskPublic]:
    """
    Get a specific task by ID for a specific user
    """
    result = await db_session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if task:
        return TaskPublic.from_orm(task)
    return None


async def update_task_by_id_and_user(
    db_session: AsyncSession,
    task_id: str,
    user_id: str,
    task_update: TaskUpdate
) -> Optional[TaskPublic]:
    """
    Update a specific task for a specific user
    """
    result = await db_session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        return None

    # Update fields that are provided
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    task.updated_at = datetime.utcnow()

    await db_session.commit()
    await db_session.refresh(task)

    return TaskPublic.from_orm(task)


async def delete_task_by_id_and_user(db_session: AsyncSession, task_id: str, user_id: str) -> bool:
    """
    Delete a specific task for a specific user
    """
    result = await db_session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        return False

    await db_session.delete(task)
    await db_session.commit()

    return True


async def toggle_task_completion(db_session: AsyncSession, task_id: str, user_id: str) -> Optional[TaskPublic]:
    """
    Toggle the completion status of a specific task for a specific user
    """
    result = await db_session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        return None

    # Toggle the completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await db_session.commit()
    await db_session.refresh(task)

    return TaskPublic.from_orm(task)