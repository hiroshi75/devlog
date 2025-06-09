"""
Message-related MCP tools for DevLog

This module provides messaging functionality including:
- Message creation and posting
- Direct messaging
- Thread management
- Read status management
- Real-time communication features
"""

from typing import Optional, List, Dict, Any

from app.db.database import SessionLocal
from app.schemas.message import MessageCreate, DirectMessageCreate, MessageUpdate
from app.models.message import Message as MessageModel
from app import crud


def create_message_tool(
    content: str,
    message_type: str = "comment",
    user_id: Optional[int] = None,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    parent_id: Optional[int] = None,
    recipient_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a new message
    
    Args:
        content: Message content
        message_type: Type of message (default: "comment")
        user_id: User ID who created the message
        project_id: Project ID this message belongs to (optional)
        task_id: Task ID this message belongs to (optional)
        parent_id: Parent message ID for threaded messages (optional)
        recipient_id: Recipient user ID for direct messages (optional)
        
    Returns:
        Created message information
        
    Raises:
        ValueError: If content is empty or user_id is missing
    """
    if not content or not content.strip():
        raise ValueError("Message content is required")
    
    if user_id is None:
        raise ValueError("User ID is required")
    
    # ダイレクトメッセージの場合の検証
    if message_type == "direct_message":
        if recipient_id is None:
            raise ValueError("Recipient ID is required for direct messages")
        if project_id is not None or task_id is not None:
            raise ValueError("Direct messages cannot belong to projects or tasks")
    
    db = SessionLocal()
    try:
        message_data = MessageCreate(
            content=content,
            message_type=message_type,
            user_id=user_id,
            recipient_id=recipient_id,
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
            "recipient_id": message.recipient_id,
            "project_id": message.project_id,
            "task_id": message.task_id,
            "parent_id": message.parent_id,
            "is_read": message.is_read,
            "is_deleted": message.is_deleted,
            "created_at": message.created_at.isoformat() if message.created_at else None,
            "updated_at": message.updated_at.isoformat() if message.updated_at else None
        }
    finally:
        db.close()


def create_direct_message_tool(
    content: str,
    user_id: int,
    recipient_id: int,
    parent_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a direct message
    
    Args:
        content: Message content
        user_id: Sender user ID
        recipient_id: Recipient user ID
        parent_id: Parent message ID for threaded DMs (optional)
        
    Returns:
        Created direct message information
        
    Raises:
        ValueError: If content is empty or user IDs are missing
    """
    if not content or not content.strip():
        raise ValueError("Message content is required")
    
    if user_id == recipient_id:
        raise ValueError("Cannot send direct message to yourself")
    
    db = SessionLocal()
    try:
        dm_data = DirectMessageCreate(
            content=content,
            user_id=user_id,
            recipient_id=recipient_id,
            parent_id=parent_id
        )
        message = crud.message.create_direct_message(db=db, dm=dm_data)
        
        return {
            "id": message.id,
            "content": message.content,
            "message_type": message.message_type,
            "user_id": message.user_id,
            "recipient_id": message.recipient_id,
            "parent_id": message.parent_id,
            "is_read": message.is_read,
            "created_at": message.created_at.isoformat() if message.created_at else None
        }
    finally:
        db.close()


def get_messages_tool(
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    user_id: Optional[int] = None,
    recipient_id: Optional[int] = None,
    message_type: Optional[str] = None,
    parent_id: Optional[int] = None,
    include_deleted: bool = False,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get messages with optional filters
    
    Args:
        project_id: Filter by project ID (optional)
        task_id: Filter by task ID (optional)
        user_id: Filter by user ID (optional)
        recipient_id: Filter by recipient ID (optional)
        message_type: Filter by message type (optional)
        parent_id: Filter by parent message ID (optional)
        include_deleted: Include deleted messages (default: False)
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
            recipient_id=recipient_id,
            message_type=message_type,
            parent_id=parent_id,
            include_deleted=include_deleted,
            limit=limit
        )
        
        return [
            {
                "id": message.id,
                "content": message.content,
                "message_type": message.message_type,
                "user_id": message.user_id,
                "recipient_id": message.recipient_id,
                "project_id": message.project_id,
                "task_id": message.task_id,
                "parent_id": message.parent_id,
                "is_read": message.is_read,
                "is_deleted": message.is_deleted,
                "created_at": message.created_at.isoformat() if message.created_at else None,
                "updated_at": message.updated_at.isoformat() if message.updated_at else None
            }
            for message in messages
        ]
    finally:
        db.close()


def get_direct_messages_tool(
    user_id: int,
    other_user_id: int,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get direct messages between two users
    
    Args:
        user_id: Current user ID
        other_user_id: Other user ID
        limit: Maximum number of messages to return (default: 100)
        
    Returns:
        List of direct messages between the users
    """
    db = SessionLocal()
    try:
        messages = crud.message.get_direct_messages(
            db=db,
            user_id=user_id,
            other_user_id=other_user_id,
            limit=limit
        )
        
        return [
            {
                "id": message.id,
                "content": message.content,
                "user_id": message.user_id,
                "recipient_id": message.recipient_id,
                "parent_id": message.parent_id,
                "is_read": message.is_read,
                "created_at": message.created_at.isoformat() if message.created_at else None
            }
            for message in messages
        ]
    finally:
        db.close()


def get_thread_messages_tool(
    parent_id: int,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get thread messages (replies to a specific message)
    
    Args:
        parent_id: Parent message ID
        limit: Maximum number of messages to return (default: 100)
        
    Returns:
        List of thread messages
    """
    db = SessionLocal()
    try:
        messages = crud.message.get_thread_messages(
            db=db,
            parent_id=parent_id,
            limit=limit
        )
        
        return [
            {
                "id": message.id,
                "content": message.content,
                "message_type": message.message_type,
                "user_id": message.user_id,
                "recipient_id": message.recipient_id,
                "project_id": message.project_id,
                "task_id": message.task_id,
                "parent_id": message.parent_id,
                "is_read": message.is_read,
                "created_at": message.created_at.isoformat() if message.created_at else None
            }
            for message in messages
        ]
    finally:
        db.close()


def get_unread_messages_tool(
    user_id: int,
    message_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get unread messages for a user
    
    Args:
        user_id: User ID to get unread messages for
        message_type: Filter by message type (optional)
        
    Returns:
        List of unread messages
    """
    db = SessionLocal()
    try:
        messages = crud.message.get_unread_messages(
            db=db,
            user_id=user_id,
            message_type=message_type
        )
        
        return [
            {
                "id": message.id,
                "content": message.content,
                "message_type": message.message_type,
                "user_id": message.user_id,
                "recipient_id": message.recipient_id,
                "project_id": message.project_id,
                "task_id": message.task_id,
                "parent_id": message.parent_id,
                "created_at": message.created_at.isoformat() if message.created_at else None
            }
            for message in messages
        ]
    finally:
        db.close()


def mark_message_as_read_tool(message_id: int) -> Dict[str, Any]:
    """
    Mark a message as read
    
    Args:
        message_id: Message ID to mark as read
        
    Returns:
        Updated message information
        
    Raises:
        ValueError: If message not found
    """
    db = SessionLocal()
    try:
        message = crud.message.mark_as_read(db=db, message_id=message_id)
        
        if not message:
            raise ValueError(f"Message not found: {message_id}")
        
        return {
            "id": message.id,
            "is_read": message.is_read,
            "updated_at": message.updated_at.isoformat() if message.updated_at else None
        }
    finally:
        db.close()


def mark_conversation_as_read_tool(user_id: int, other_user_id: int) -> Dict[str, Any]:
    """
    Mark all messages in a conversation as read
    
    Args:
        user_id: Current user ID
        other_user_id: Other user ID in the conversation
        
    Returns:
        Number of messages marked as read
    """
    db = SessionLocal()
    try:
        count = crud.message.mark_conversation_as_read(
            db=db,
            user_id=user_id,
            other_user_id=other_user_id
        )
        
        return {
            "messages_marked_read": count
        }
    finally:
        db.close()


def delete_message_tool(message_id: int) -> Dict[str, Any]:
    """
    Delete a message (soft delete)
    
    Args:
        message_id: Message ID to delete
        
    Returns:
        Updated message information
        
    Raises:
        ValueError: If message not found
    """
    db = SessionLocal()
    try:
        message = crud.message.mark_as_deleted(db=db, message_id=message_id)
        
        if not message:
            raise ValueError(f"Message not found: {message_id}")
        
        return {
            "id": message.id,
            "is_deleted": message.is_deleted,
            "updated_at": message.updated_at.isoformat() if message.updated_at else None
        }
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
            "recipient_id": message.recipient_id,
            "project_id": message.project_id,
            "task_id": message.task_id,
            "parent_id": message.parent_id,
            "is_read": message.is_read,
            "is_deleted": message.is_deleted,
            "created_at": message.created_at.isoformat() if message.created_at else None,
            "updated_at": message.updated_at.isoformat() if message.updated_at else None
        }
    finally:
        db.close() 