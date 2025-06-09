"""
メッセージのCRUD操作
"""
from typing import List, Optional, Union
from sqlalchemy.orm import Session, joinedload

from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate, DirectMessageCreate, MessageUpdate


def get_message(db: Session, message_id: int) -> Optional[Message]:
    """IDによるメッセージの取得"""
    return db.query(Message).filter(Message.id == message_id, Message.is_deleted == False).first()


def get_messages(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    user_id: Optional[int] = None,
    recipient_id: Optional[int] = None,
    message_type: Optional[str] = None,
    parent_id: Optional[int] = None,
    include_deleted: bool = False
) -> List[Message]:
    """メッセージリストの取得"""
    query = db.query(Message)
    
    if not include_deleted:
        query = query.filter(Message.is_deleted == False)
    
    if project_id is not None:
        query = query.filter(Message.project_id == project_id)
    
    if task_id is not None:
        query = query.filter(Message.task_id == task_id)
    
    if user_id is not None:
        query = query.filter(Message.user_id == user_id)
    
    if recipient_id is not None:
        query = query.filter(Message.recipient_id == recipient_id)
    
    if message_type is not None:
        query = query.filter(Message.message_type == message_type)
    
    if parent_id is not None:
        query = query.filter(Message.parent_id == parent_id)
    
    return query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()


def get_direct_messages(
    db: Session,
    user_id: int,
    other_user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Message]:
    """2ユーザー間のダイレクトメッセージを取得"""
    return db.query(Message).filter(
        Message.is_deleted == False,
        Message.message_type == "direct_message",
        (
            (Message.user_id == user_id) & (Message.recipient_id == other_user_id) |
            (Message.user_id == other_user_id) & (Message.recipient_id == user_id)
        )
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()


def get_thread_messages(
    db: Session,
    parent_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Message]:
    """スレッドメッセージを取得"""
    return db.query(Message).filter(
        Message.parent_id == parent_id,
        Message.is_deleted == False
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()


def get_unread_messages(
    db: Session,
    user_id: int,
    message_type: Optional[str] = None
) -> List[Message]:
    """未読メッセージを取得"""
    query = db.query(Message).filter(
        Message.recipient_id == user_id,
        Message.is_read == False,
        Message.is_deleted == False
    )
    
    if message_type:
        query = query.filter(Message.message_type == message_type)
    
    return query.order_by(Message.created_at.desc()).all()


def create_message(db: Session, message: MessageCreate) -> Message:
    """メッセージの作成"""
    db_message = Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def create_direct_message(db: Session, dm: DirectMessageCreate) -> Message:
    """ダイレクトメッセージの作成"""
    db_message = Message(
        content=dm.content,
        message_type="direct_message",
        user_id=dm.user_id,
        recipient_id=dm.recipient_id,
        parent_id=dm.parent_id,
        project_id=None,
        task_id=None
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(db: Session, message_id: int, message_update: MessageUpdate) -> Optional[Message]:
    """メッセージの更新"""
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if not db_message:
        return None
    
    update_data = message_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_message, field, value)
    
    db.commit()
    db.refresh(db_message)
    return db_message


def mark_as_read(db: Session, message_id: int) -> Optional[Message]:
    """メッセージを既読にする"""
    return update_message(db, message_id, MessageUpdate(is_read=True))


def mark_as_deleted(db: Session, message_id: int) -> Optional[Message]:
    """メッセージを論理削除する"""
    return update_message(db, message_id, MessageUpdate(is_deleted=True))


def mark_conversation_as_read(db: Session, user_id: int, other_user_id: int) -> int:
    """会話の全メッセージを既読にする"""
    count = db.query(Message).filter(
        Message.user_id == other_user_id,
        Message.recipient_id == user_id,
        Message.is_read == False,
        Message.is_deleted == False
    ).update({Message.is_read: True})
    
    db.commit()
    return count 