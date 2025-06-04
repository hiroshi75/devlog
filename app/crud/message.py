"""
メッセージのCRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate


def get_message(db: Session, message_id: int) -> Optional[Message]:
    """IDによるメッセージの取得"""
    return db.query(Message).filter(Message.id == message_id).first()


def get_messages(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    user_id: Optional[int] = None,
    message_type: Optional[str] = None,
    parent_id: Optional[int] = None
) -> List[Message]:
    """メッセージリストの取得"""
    query = db.query(Message)
    
    if project_id is not None:
        query = query.filter(Message.project_id == project_id)
    
    if task_id is not None:
        query = query.filter(Message.task_id == task_id)
    
    if user_id is not None:
        query = query.filter(Message.user_id == user_id)
    
    if message_type is not None:
        query = query.filter(Message.message_type == message_type)
    
    if parent_id is not None:
        query = query.filter(Message.parent_id == parent_id)
    
    return query.offset(skip).limit(limit).all()


def create_message(db: Session, message: MessageCreate) -> Message:
    """メッセージの作成"""
    db_message = Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message 