"""
プロジェクトモデルの定義
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.database import Base


class Project(Base):
    """プロジェクトモデル"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # リレーションシップ
    tasks = relationship("Task", back_populates="project")
    messages = relationship("Message", back_populates="project")
    
    def __str__(self):
        """文字列表現"""
        return f"<Project(name='{self.name}')>"
    
    def __repr__(self):
        """開発者向けの文字列表現"""
        return self.__str__() 