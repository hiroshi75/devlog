"""
ユーザー関連のPydanticスキーマ定義

このモジュールは、ユーザーのCRUD操作で使用される
リクエスト/レスポンススキーマを定義します。
"""
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    """
    ユーザーの基本スキーマ
    
    作成時の共通フィールドを定義します。
    """
    username: str = Field(..., min_length=1, max_length=100, description="ユーザー名")
    email: EmailStr = Field(..., description="メールアドレス")


class UserCreate(UserBase):
    """
    ユーザー作成時のスキーマ
    
    新規ユーザー作成時のリクエストボディで使用されます。
    """
    pass


class User(UserBase):
    """
    ユーザーのレスポンススキーマ
    
    データベースから取得したユーザー情報を返す際に使用されます。
    """
    id: int = Field(..., description="ユーザーID")
    created_at: datetime = Field(..., description="作成日時")
    
    model_config = ConfigDict(from_attributes=True) 