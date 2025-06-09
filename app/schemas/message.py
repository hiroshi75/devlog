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
    DIRECT_MESSAGE = "direct_message"
    TASK_UPDATE = "task_update"
    STATUS_CHANGE = "status_change"


class MessageBase(BaseModel):
    """
    メッセージの基本スキーマ
    
    作成時の共通フィールドを定義します。
    """
    content: str = Field(..., min_length=1, description="メッセージ内容")
    message_type: MessageType = Field(..., description="メッセージタイプ")
    user_id: int = Field(..., description="投稿者ID")
    recipient_id: Optional[int] = Field(None, description="ダイレクトメッセージの宛先ユーザーID")
    project_id: Optional[int] = Field(None, description="プロジェクトID")
    task_id: Optional[int] = Field(None, description="関連タスクID")
    parent_id: Optional[int] = Field(None, description="親メッセージID（スレッド用）")


class MessageCreate(MessageBase):
    """
    メッセージ作成時のスキーマ
    
    新規メッセージ作成時のリクエストボディで使用されます。
    """
    pass


class DirectMessageCreate(BaseModel):
    """
    ダイレクトメッセージ作成時のスキーマ
    """
    content: str = Field(..., min_length=1, description="メッセージ内容")
    user_id: int = Field(..., description="送信者ID")
    recipient_id: int = Field(..., description="受信者ID")
    parent_id: Optional[int] = Field(None, description="親メッセージID（スレッド用）")


class MessageUpdate(BaseModel):
    """
    メッセージ更新用のスキーマ
    """
    is_read: Optional[bool] = Field(None, description="既読状態")
    is_deleted: Optional[bool] = Field(None, description="削除状態")


class Message(MessageBase):
    """
    メッセージのレスポンススキーマ
    
    データベースから取得したメッセージ情報を返す際に使用されます。
    """
    id: int = Field(..., description="メッセージID")
    is_read: bool = Field(default=False, description="既読状態")
    is_deleted: bool = Field(default=False, description="削除状態")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    
    model_config = ConfigDict(from_attributes=True)


class MessageWithUser(Message):
    """
    ユーザー情報付きメッセージのレスポンススキーマ
    """
    user_name: str = Field(..., description="投稿者名")
    recipient_name: Optional[str] = Field(None, description="受信者名") 