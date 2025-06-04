"""
Message API endpoints
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import message as crud_message
from app.db.database import get_db
from app.schemas.message import Message, MessageCreate

router = APIRouter()


@router.post("/", response_model=Message, status_code=status.HTTP_201_CREATED)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new message"""
    return crud_message.create_message(db=db, message=message)


@router.get("/", response_model=List[Message])
def get_messages(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all messages with optional filters"""
    messages = crud_message.get_messages(
        db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        task_id=task_id,
        user_id=user_id
    )
    return messages


@router.get("/{message_id}", response_model=Message)
def get_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific message by ID"""
    db_message = crud_message.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    return db_message 