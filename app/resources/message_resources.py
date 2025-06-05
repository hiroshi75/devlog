"""
Message-related MCP resources for DevStatusMCP
"""

from typing import Dict, Any, Optional, List

from app.db.database import get_db
from app.models.message import Message as MessageModel
from app import crud


def messages_recent_resource_handler(
    limit: int = 50,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    user_id: Optional[int] = None,
    message_type: Optional[str] = None,
    include_user_info: bool = False
) -> Dict[str, Any]:
    """
    Handle recent messages resource requests
    
    Args:
        limit: Maximum number of messages to retrieve (default: 50)
        project_id: Filter by project ID (optional)
        task_id: Filter by task ID (optional)
        user_id: Filter by user ID (optional)
        message_type: Filter by message type (optional)
        include_user_info: Whether to include user information for each message
        
    Returns:
        Recent messages information as dictionary
    """
    db = next(get_db())
    try:
        # Get messages with filters
        messages = crud.message.get_messages(
            db=db,
            project_id=project_id,
            task_id=task_id,
            user_id=user_id,
            message_type=message_type,
            limit=limit
        )
        
        # Build messages response
        message_list = []
        for message in messages:
            message_dict = {
                "id": message.id,
                "content": message.content,
                "message_type": message.message_type,
                "user_id": message.user_id,
                "project_id": message.project_id,
                "task_id": message.task_id,
                "parent_id": message.parent_id,
                "created_at": message.created_at.isoformat() if message.created_at else None
            }
            
            # Include user information if requested
            if include_user_info and message.user_id:
                user = crud.user.get_user(db=db, user_id=message.user_id)
                if user:
                    message_dict["user"] = {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
            
            message_list.append(message_dict)
        
        # Build response
        result = {
            "messages": message_list,
            "total_count": len(message_list),
            "limit": limit
        }
        
        # Add filter information if any filters were applied
        if project_id or task_id or user_id or message_type:
            result["filters"] = {}
            if project_id:
                result["filters"]["project_id"] = project_id
            if task_id:
                result["filters"]["task_id"] = task_id
            if user_id:
                result["filters"]["user_id"] = user_id
            if message_type:
                result["filters"]["message_type"] = message_type
        
        return result
    finally:
        db.close() 