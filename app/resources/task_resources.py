"""
Task-related MCP resources for DevLog

This module provides read-only access to task information including:
- Task details and status
- Task dependencies and relationships
- Task progress and history
"""

from typing import Dict, Any, Optional

from app.db.database import get_db
from app.models.task import Task as TaskModel
from app import crud


def task_resource_handler(
    task_id: Any,
    include_messages: bool = False,
    include_project: bool = False
) -> Dict[str, Any]:
    """
    Handle task resource requests
    
    Args:
        task_id: Task ID to retrieve
        include_messages: Whether to include related messages (optional)
        include_project: Whether to include project information (optional)
        
    Returns:
        Task information as dictionary
        
    Raises:
        ValueError: If task ID is invalid or task not found
    """
    # Validate task_id
    try:
        task_id = int(task_id)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid task ID: {task_id}")
    
    db = next(get_db())
    try:
        # Get task
        task = crud.task.get_task(db=db, task_id=task_id)
        
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        # Build response
        result = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "project_id": task.project_id,
            "assignee_id": task.assignee_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }
        
        # Include messages if requested
        if include_messages:
            messages = crud.message.get_messages(db=db, task_id=task_id)
            result["messages"] = [
                {
                    "id": message.id,
                    "content": message.content,
                    "message_type": message.message_type,
                    "user_id": message.user_id,
                    "created_at": message.created_at.isoformat() if message.created_at else None
                }
                for message in messages
            ]
        
        # Include project information if requested
        if include_project and task.project_id:
            project = crud.project.get_project(db=db, project_id=task.project_id)
            if project:
                result["project"] = {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description
                }
        
        return result
    finally:
        db.close() 