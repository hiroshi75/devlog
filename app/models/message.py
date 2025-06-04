"""
メッセージモデルの定義
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Message(Base):
    """メッセージモデル"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False)  # comment, task_update, status_change, announcement
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # リレーションシップ
    user = relationship("User", back_populates="messages")
    task = relationship("Task", back_populates="messages")
    project = relationship("Project", back_populates="messages")
    parent = relationship("Message", remote_side=[id], backref="replies")
    
    def __str__(self):
        """文字列表現"""
        return f"<Message(type='{self.message_type}', user_id={self.user_id}, project_id={self.project_id})>"
    
    def __repr__(self):
        """開発者向けの文字列表現"""
        return self.__str__() 