"""
メッセージ関連のPydanticスキーマ定義

このモジュールは、メッセージのCRUD操作で使用される
リクエスト/レスポンススキーマを定義します。
"""
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class MessageType(str, Enum):
    """メッセージのタイプ定義"""
    STATUS_UPDATE = "status_update"
    COMMENT = "comment"
    QUESTION = "question"
    ANSWER = "answer"
    ANNOUNCEMENT = "announcement"


class MessageBase(BaseModel):
    """
    メッセージの基本スキーマ
    
    作成時の共通フィールドを定義します。
    """
    content: str = Field(..., min_length=1, description="メッセージ内容")
    message_type: MessageType = Field(..., description="メッセージタイプ")
    user_id: int = Field(..., description="投稿者ID")
    project_id: Optional[int] = Field(None, description="プロジェクトID")
    task_id: Optional[int] = Field(None, description="関連タスクID")
    parent_id: Optional[int] = Field(None, description="親メッセージID（スレッド用）")


class MessageCreate(MessageBase):
    """
    メッセージ作成時のスキーマ
    
    新規メッセージ作成時のリクエストボディで使用されます。
    """
    pass


class Message(MessageBase):
    """
    メッセージのレスポンススキーマ
    
    データベースから取得したメッセージ情報を返す際に使用されます。
    """
    id: int = Field(..., description="メッセージID")
    created_at: datetime = Field(..., description="作成日時")
    
    model_config = ConfigDict(from_attributes=True) 