"""
Userスキーマのテスト

UserBase, UserCreate, Userスキーマの
バリデーションと動作をテストします。
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.user import UserBase, UserCreate, User


class TestUserBase:
    """UserBaseスキーマのテスト"""
    
    def test_valid_user_base(self):
        """有効なUserBaseの作成"""
        user = UserBase(
            username="testuser",
            email="test@example.com"
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
    
    def test_user_base_empty_username(self):
        """空のユーザー名でエラー"""
        with pytest.raises(ValidationError):
            UserBase(username="", email="test@example.com")
    
    def test_user_base_invalid_email(self):
        """無効なメールアドレスでエラー"""
        with pytest.raises(ValidationError):
            UserBase(username="testuser", email="invalid-email")
    
    def test_user_base_missing_fields(self):
        """必須フィールドなしでエラー"""
        with pytest.raises(ValidationError):
            UserBase(username="testuser")
        
        with pytest.raises(ValidationError):
            UserBase(email="test@example.com")


class TestUserCreate:
    """UserCreateスキーマのテスト"""
    
    def test_valid_user_create(self):
        """有効なUserCreateの作成"""
        user = UserCreate(
            username="newuser",
            email="newuser@example.com"
        )
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
    
    def test_user_create_inherits_from_base(self):
        """UserBaseを継承していることを確認"""
        assert issubclass(UserCreate, UserBase)


class TestUser:
    """Userレスポンススキーマのテスト"""
    
    def test_valid_user_response(self):
        """有効なUserレスポンスの作成"""
        now = datetime.now()
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            created_at=now
        )
        assert user.id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.created_at == now
    
    def test_user_inherits_from_base(self):
        """UserBaseを継承していることを確認"""
        assert issubclass(User, UserBase)
    
    def test_user_from_orm_mode(self):
        """ORMモードが有効であることを確認"""
        assert hasattr(User, 'model_config')
        assert User.model_config.get('from_attributes', False) is True 