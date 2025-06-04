"""
Task API endpoints
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import task as crud_task
from app.db.database import get_db
from app.schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """Create a new task"""
    return crud_task.create_task(db=db, task=task)


@router.get("/", response_model=List[Task])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all tasks with optional filters"""
    tasks = crud_task.get_tasks(
        db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        assignee_id=assignee_id
    )
    return tasks


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific task by ID"""
    db_task = crud_task.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update a task"""
    db_task = crud_task.update_task(
        db=db,
        task_id=task_id,
        task=task
    )
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Delete a task"""
    success = crud_task.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return None 