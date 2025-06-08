"""
Message-related MCP tools for DevLog

This module provides messaging functionality including:
- Message creation and posting
- Thread management
- Real-time communication features
"""

from typing import Optional, List, Dict, Any

from app.db.database import SessionLocal
from app.schemas.message import MessageCreate
from app.models.message import Message as MessageModel
from app import crud


def create_message_tool(
    content: str,
    message_type: str = "status_update",
    user_id: Optional[int] = None,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    parent_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a new message
    
    Args:
        content: Message content
        message_type: Type of message (default: "status_update")
        user_id: User ID who created the message
        project_id: Project ID this message belongs to (optional)
        task_id: Task ID this message belongs to (optional)
        parent_id: Parent message ID for threaded messages (optional)
        
    Returns:
        Created message information
        
    Raises:
        ValueError: If content is empty or user_id is missing
    """
    if not content or not content.strip():
        raise ValueError("Message content is required")
    
    if user_id is None:
        raise ValueError("User ID is required")
    
    db = SessionLocal()
    try:
        message_data = MessageCreate(
            content=content,
            message_type=message_type,
            user_id=user_id,
            project_id=project_id,
            task_id=task_id,
            parent_id=parent_id
        )
        message = crud.message.create_message(db=db, message=message_data)
        
        return {
            "id": message.id,
            "content": message.content,
            "message_type": message.message_type,
            "user_id": message.user_id,
            "project_id": message.project_id,
            "task_id": message.task_id,
            "parent_id": message.parent_id,
            "created_at": message.created_at.isoformat() if message.created_at else None
        }
    finally:
        db.close()


def get_messages_tool(
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    user_id: Optional[int] = None,
    message_type: Optional[str] = None,
    parent_id: Optional[int] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get messages with optional filters
    
    Args:
        project_id: Filter by project ID (optional)
        task_id: Filter by task ID (optional)
        user_id: Filter by user ID (optional)
        message_type: Filter by message type (optional)
        parent_id: Filter by parent message ID (optional)
        limit: Maximum number of messages to return (default: 100)
        
    Returns:
        List of messages matching the filters
    """
    db = SessionLocal()
    try:
        messages = crud.message.get_messages(
            db=db,
            project_id=project_id,
            task_id=task_id,
            user_id=user_id,
            message_type=message_type,
            parent_id=parent_id,
            limit=limit
        )
        
        return [
            {
                "id": message.id,
                "content": message.content,
                "message_type": message.message_type,
                "user_id": message.user_id,
                "project_id": message.project_id,
                "task_id": message.task_id,
                "parent_id": message.parent_id,
                "created_at": message.created_at.isoformat() if message.created_at else None
            }
            for message in messages
        ]
    finally:
        db.close()


def get_message_tool(message_id: int) -> Dict[str, Any]:
    """
    Get a specific message by ID
    
    Args:
        message_id: Message ID
        
    Returns:
        Message information
        
    Raises:
        ValueError: If message not found
    """
    db = SessionLocal()
    try:
        message = crud.message.get_message(db=db, message_id=message_id)
        
        if not message:
            raise ValueError(f"Message not found: {message_id}")
        
        return {
            "id": message.id,
            "content": message.content,
            "message_type": message.message_type,
            "user_id": message.user_id,
            "project_id": message.project_id,
            "task_id": message.task_id,
            "parent_id": message.parent_id,
            "created_at": message.created_at.isoformat() if message.created_at else None
        }
    finally:
        db.close() 