from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.task import Task, TaskPublic
from src.schemas.task import TaskCreate, TaskUpdate
from datetime import datetime
import uuid

def create_task(db_session: Session, task_create: TaskCreate, user_id: str) -> TaskPublic:
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
    db_session.commit()
    db_session.refresh(task)

    return TaskPublic.from_orm(task)


def get_tasks_by_user(db_session: Session, user_id: str) -> List[TaskPublic]:
    """
    Get all tasks for a specific user
    """
    tasks = db_session.query(Task).filter(Task.user_id == user_id).all()

    return [TaskPublic.from_orm(task) for task in tasks]


def get_task_by_id_and_user(db_session: Session, task_id: str, user_id: str) -> Optional[TaskPublic]:
    """
    Get a specific task by ID for a specific user
    """
    task = db_session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if task:
        return TaskPublic.from_orm(task)
    return None


def update_task_by_id_and_user(
    db_session: Session,
    task_id: str,
    user_id: str,
    task_update: TaskUpdate
) -> Optional[TaskPublic]:
    """
    Update a specific task for a specific user
    """
    task = db_session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

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

    db_session.commit()
    db_session.refresh(task)

    return TaskPublic.from_orm(task)


def delete_task_by_id_and_user(db_session: Session, task_id: str, user_id: str) -> bool:
    """
    Delete a specific task for a specific user
    """
    task = db_session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        return False

    db_session.delete(task)
    db_session.commit()

    return True


def toggle_task_completion(db_session: Session, task_id: str, user_id: str) -> Optional[TaskPublic]:
    """
    Toggle the completion status of a specific task for a specific user
    """
    task = db_session.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        return None

    # Toggle the completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    db_session.commit()
    db_session.refresh(task)

    return TaskPublic.from_orm(task)