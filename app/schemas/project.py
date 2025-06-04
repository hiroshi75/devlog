"""
プロジェクト関連のPydanticスキーマ定義

このモジュールは、プロジェクトのCRUD操作で使用される
リクエスト/レスポンススキーマを定義します。
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):
    """
    プロジェクトの基本スキーマ
    
    作成・更新時の共通フィールドを定義します。
    """
    name: str = Field(..., min_length=1, max_length=255, description="プロジェクト名")
    description: Optional[str] = Field(None, description="プロジェクトの説明")


class ProjectCreate(ProjectBase):
    """
    プロジェクト作成時のスキーマ
    
    新規プロジェクト作成時のリクエストボディで使用されます。
    """
    pass


class ProjectUpdate(BaseModel):
    """
    プロジェクト更新時のスキーマ
    
    部分更新をサポートするため、全フィールドがオプショナルです。
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="プロジェクト名")
    description: Optional[str] = Field(None, description="プロジェクトの説明")


class Project(ProjectBase):
    """
    プロジェクトのレスポンススキーマ
    
    データベースから取得したプロジェクト情報を返す際に使用されます。
    """
    id: int = Field(..., description="プロジェクトID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    
    model_config = ConfigDict(from_attributes=True) 