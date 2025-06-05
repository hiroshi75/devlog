"""
User-related MCP resources for DevLog

This module provides read-only access to user information including:
- User profiles and basic information
- User activity and status
- User relationships and permissions
"""

from typing import Dict, Any, Optional, Union

from app.db.database import get_db
from app.models.user import User as UserModel
from app import crud


def user_resource_handler(
    user_identifier: Union[int, str],
    lookup_by_username: bool = False,
    include_tasks: bool = False,
    include_messages: bool = False
) -> Dict[str, Any]:
    """
    Handle user resource requests
    
    Args:
        user_identifier: User ID (int) or username (str) to retrieve
        lookup_by_username: Whether to lookup by username instead of ID
        include_tasks: Whether to include assigned tasks (optional)
        include_messages: Whether to include user messages (optional)
        
    Returns:
        User information as dictionary
        
    Raises:
        ValueError: If user identifier is invalid or user not found
    """
    db = next(get_db())
    try:
        # Get user based on lookup type
        if lookup_by_username:
            if not isinstance(user_identifier, str):
                raise ValueError(f"Invalid username: {user_identifier}")
            user = crud.user.get_user_by_username(db=db, username=user_identifier)
        else:
            # Validate user_id
            try:
                user_id = int(user_identifier)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid user ID: {user_identifier}")
            user = crud.user.get_user(db=db, user_id=user_id)
        
        if not user:
            identifier_type = "username" if lookup_by_username else "user ID"
            raise ValueError(f"User not found: {identifier_type} {user_identifier}")
        
        # Build response
        result = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        
        # Include tasks if requested
        if include_tasks:
            tasks = crud.task.get_tasks(db=db, assignee_id=user.id)
            result["tasks"] = [
                {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "project_id": task.project_id,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                }
                for task in tasks
            ]
        
        # Include messages if requested
        if include_messages:
            messages = crud.message.get_messages(db=db, user_id=user.id, limit=50)
            result["messages"] = [
                {
                    "id": message.id,
                    "content": message.content,
                    "message_type": message.message_type,
                    "project_id": message.project_id,
                    "task_id": message.task_id,
                    "created_at": message.created_at.isoformat() if message.created_at else None
                }
                for message in messages
            ]
        
        return result
    finally:
        db.close() 