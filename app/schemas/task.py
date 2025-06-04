"""
タスク関連のPydanticスキーマ定義

このモジュールは、タスクのCRUD操作で使用される
リクエスト/レスポンススキーマを定義します。
"""
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    """タスクのステータス定義"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskBase(BaseModel):
    """
    タスクの基本スキーマ
    
    作成・更新時の共通フィールドを定義します。
    """
    title: str = Field(..., min_length=1, max_length=255, description="タスクタイトル")
    description: Optional[str] = Field(None, description="タスクの説明")
    status: TaskStatus = Field(..., description="タスクのステータス")
    project_id: int = Field(..., description="所属プロジェクトID")
    assignee_id: Optional[int] = Field(None, description="担当者ID")


class TaskCreate(TaskBase):
    """
    タスク作成時のスキーマ
    
    新規タスク作成時のリクエストボディで使用されます。
    """
    pass


class TaskUpdate(BaseModel):
    """
    タスク更新時のスキーマ
    
    部分更新をサポートするため、全フィールドがオプショナルです。
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="タスクタイトル")
    description: Optional[str] = Field(None, description="タスクの説明")
    status: Optional[TaskStatus] = Field(None, description="タスクのステータス")
    assignee_id: Optional[int] = Field(None, description="担当者ID")


class Task(TaskBase):
    """
    タスクのレスポンススキーマ
    
    データベースから取得したタスク情報を返す際に使用されます。
    """
    id: int = Field(..., description="タスクID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    
    model_config = ConfigDict(from_attributes=True) 