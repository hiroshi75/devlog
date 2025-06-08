"""
ユーザーモデルの定義
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    """ユーザーモデル"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # リレーションシップ
    assigned_tasks = relationship("Task", back_populates="assignee")
    messages = relationship("Message", back_populates="user")
    
    def __str__(self):
        """文字列表現"""
        return f"<User(username='{self.username}', email='{self.email}')>"
    
    def __repr__(self):
        """開発者向けの文字列表現"""
        return self.__str__() 