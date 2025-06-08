"""
User-related MCP tools for DevLog

This module provides user management functionality including:
- User registration and authentication  
- User profile management
- User status and activity tracking
"""

import re
from typing import Optional, List, Dict, Any

from app.db.database import SessionLocal
from app.schemas.user import UserCreate
from app.models.user import User as UserModel
from app import crud


def create_user_tool(username: str, email: str) -> Dict[str, Any]:
    """
    Create a new user
    
    Args:
        username: Username
        email: Email address
        
    Returns:
        Created user information
        
    Raises:
        ValueError: If username or email is empty, or email format is invalid
    """
    if not username or not username.strip():
        raise ValueError("Username is required")
    
    if not email or not email.strip():
        raise ValueError("Email is required")
    
    # Simple email format validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")
    
    db = SessionLocal()
    try:
        user_data = UserCreate(username=username, email=email)
        user = crud.user.create_user(db=db, user=user_data)
        
        if not user:
            raise ValueError("User with this username or email already exists")
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    finally:
        db.close()


def get_users_tool() -> List[Dict[str, Any]]:
    """
    Get all users
    
    Returns:
        List of all users
    """
    db = SessionLocal()
    try:
        users = crud.user.get_users(db=db)
        
        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
            for user in users
        ]
    finally:
        db.close()


def get_user_tool(
    user_id: Optional[int] = None,
    username: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a specific user by ID or username
    
    Args:
        user_id: User ID (optional)
        username: Username (optional)
        
    Returns:
        User information
        
    Raises:
        ValueError: If neither user_id nor username is provided, or user not found
    """
    if user_id is None and username is None:
        raise ValueError("Either user_id or username must be provided")
    
    db = SessionLocal()
    try:
        if user_id is not None:
            user = crud.user.get_user(db=db, user_id=user_id)
        else:
            user = crud.user.get_user_by_username(db=db, username=username)
        
        if not user:
            identifier = f"user_id={user_id}" if user_id is not None else f"username={username}"
            raise ValueError(f"User not found: {identifier}")
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    finally:
        db.close() 