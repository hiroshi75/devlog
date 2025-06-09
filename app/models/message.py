"""
メッセージモデルの定義
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class Message(Base):
    """メッセージモデル"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False)  # comment, task_update, status_change, announcement, direct_message
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # ダイレクトメッセージの宛先
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)  # 既読状態
    is_deleted = Column(Boolean, default=False, nullable=False)  # 論理削除フラグ
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # リレーションシップ
    user = relationship("User", back_populates="messages", foreign_keys=[user_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
    task = relationship("Task", back_populates="messages")
    project = relationship("Project", back_populates="messages")
    parent = relationship("Message", remote_side=[id], backref="replies")
    
    def __str__(self):
        """文字列表現"""
        return f"<Message(type='{self.message_type}', user_id={self.user_id}, project_id={self.project_id}, recipient_id={self.recipient_id})>"
    
    def __repr__(self):
        """開発者向けの文字列表現"""
        return self.__str__()
    
    @property
    def is_direct_message(self) -> bool:
        """ダイレクトメッセージかどうかを判定"""
        return self.message_type == "direct_message" and self.recipient_id is not None
    
    @property
    def is_thread_reply(self) -> bool:
        """スレッドの返信かどうかを判定"""
        return self.parent_id is not None
    
    @property
    def is_project_message(self) -> bool:
        """プロジェクトメッセージかどうかを判定"""
        return self.project_id is not None and not self.is_direct_message
    
    @property
    def is_task_message(self) -> bool:
        """タスクメッセージかどうかを判定"""
        return self.task_id is not None 