"""
Task-related MCP tools for DevLog

This module provides task management functionality including:
- Task creation and assignment
- Task status updates and tracking
- Task dependencies and relationships
"""

from typing import Optional, List, Dict, Any

from app.db.database import SessionLocal
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task as TaskModel
from app import crud


def create_task_tool(
    title: str,
    project_id: int,
    description: Optional[str] = None,
    status: str = "pending",
    assignee_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a new task
    
    Args:
        title: Task title
        project_id: Project ID this task belongs to
        description: Task description (optional)
        status: Task status (default: "pending")
        assignee_id: User ID of the assignee (optional)
        
    Returns:
        Created task information
        
    Raises:
        ValueError: If task title is empty
    """
    if not title or not title.strip():
        raise ValueError("Task title is required")
    
    db = SessionLocal()
    try:
        task_data = TaskCreate(
            title=title,
            description=description,
            status=status,
            project_id=project_id,
            assignee_id=assignee_id
        )
        task = crud.task.create_task(db=db, task=task_data)
        
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "project_id": task.project_id,
            "assignee_id": task.assignee_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }
    finally:
        db.close()


def get_tasks_tool(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    assignee_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get tasks with optional filters
    
    Args:
        project_id: Filter by project ID (optional)
        status: Filter by status (optional)
        assignee_id: Filter by assignee ID (optional)
        
    Returns:
        List of tasks matching the filters
    """
    db = SessionLocal()
    try:
        tasks = crud.task.get_tasks(
            db=db,
            project_id=project_id,
            status=status,
            assignee_id=assignee_id
        )
        
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "project_id": task.project_id,
                "assignee_id": task.assignee_id,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            for task in tasks
        ]
    finally:
        db.close()


def get_task_tool(task_id: int) -> Dict[str, Any]:
    """
    Get a specific task by ID
    
    Args:
        task_id: Task ID
        
    Returns:
        Task information
        
    Raises:
        ValueError: If task not found
    """
    db = SessionLocal()
    try:
        task = crud.task.get_task(db=db, task_id=task_id)
        
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "project_id": task.project_id,
            "assignee_id": task.assignee_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }
    finally:
        db.close()


def update_task_tool(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    assignee_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Update a task
    
    Args:
        task_id: Task ID to update
        title: New task title (optional)
        description: New task description (optional)
        status: New task status (optional)
        assignee_id: New assignee ID (optional)
        
    Returns:
        Updated task information
        
    Raises:
        ValueError: If task not found
    """
    db = SessionLocal()
    try:
        # Check if task exists
        existing_task = crud.task.get_task(db=db, task_id=task_id)
        if not existing_task:
            raise ValueError(f"Task not found: {task_id}")
        
        # Create update data
        update_data = TaskUpdate()
        if title is not None:
            update_data.title = title
        if description is not None:
            update_data.description = description
        if status is not None:
            update_data.status = status
        if assignee_id is not None:
            update_data.assignee_id = assignee_id
        
        # Update task
        task = crud.task.update_task(
            db=db,
            task_id=task_id,
            task=update_data
        )
        
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "project_id": task.project_id,
            "assignee_id": task.assignee_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }
    finally:
        db.close()


def delete_task_tool(task_id: int) -> Dict[str, Any]:
    """
    Delete a task
    
    Args:
        task_id: Task ID to delete
        
    Returns:
        Deletion result
        
    Raises:
        ValueError: If task not found
    """
    db = SessionLocal()
    try:
        # Check if task exists
        existing_task = crud.task.get_task(db=db, task_id=task_id)
        if not existing_task:
            raise ValueError(f"Task not found: {task_id}")
        
        # Delete task
        success = crud.task.delete_task(db=db, task_id=task_id)
        
        return {
            "success": success,
            "message": f"Task {task_id} deleted successfully" if success else f"Failed to delete task {task_id}"
        }
    finally:
        db.close() 