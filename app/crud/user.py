"""
ユーザーのCRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int) -> Optional[User]:
    """IDによるユーザーの取得"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """メールアドレスによるユーザーの取得"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """ユーザー名によるユーザーの取得"""
    return db.query(User).filter(User.username == username).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    username: Optional[str] = None,
    email: Optional[str] = None
) -> List[User]:
    """ユーザーリストの取得"""
    query = db.query(User)
    
    if username is not None:
        query = query.filter(User.username == username)
    
    if email is not None:
        query = query.filter(User.email == email)
    
    return query.offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> Optional[User]:
    """ユーザーの作成"""
    # 重複チェック
    if get_user_by_email(db, email=user.email):
        return None
    if get_user_by_username(db, username=user.username):
        return None
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user 