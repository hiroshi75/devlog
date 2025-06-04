"""
ユーザーCRUD操作のテスト
"""
import pytest
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.schemas.user import UserCreate
from app.models.user import User


class TestUserCRUD:
    """ユーザーCRUD操作のテストクラス"""

    def test_get_user_by_id(self, db: Session):
        """IDによるユーザー取得のテスト"""
        # Arrange
        user = User(username="testuser", email="test@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Act
        result = crud_user.get_user(db, user_id=user.id)
        
        # Assert
        assert result is not None
        assert result.id == user.id
        assert result.username == "testuser"
        assert result.email == "test@example.com"

    def test_get_user_not_found(self, db: Session):
        """存在しないユーザーの取得テスト"""
        # Act
        result = crud_user.get_user(db, user_id=999)
        
        # Assert
        assert result is None

    def test_get_user_by_email(self, db: Session):
        """メールアドレスによるユーザー取得のテスト"""
        # Arrange
        user = User(username="testuser", email="test@example.com")
        db.add(user)
        db.commit()
        
        # Act
        result = crud_user.get_user_by_email(db, email="test@example.com")
        
        # Assert
        assert result is not None
        assert result.username == "testuser"
        assert result.email == "test@example.com"

    def test_get_user_by_email_not_found(self, db: Session):
        """存在しないメールアドレスでのユーザー取得テスト"""
        # Act
        result = crud_user.get_user_by_email(db, email="notfound@example.com")
        
        # Assert
        assert result is None

    def test_get_user_by_username(self, db: Session):
        """ユーザー名によるユーザー取得のテスト"""
        # Arrange
        user = User(username="testuser", email="test@example.com")
        db.add(user)
        db.commit()
        
        # Act
        result = crud_user.get_user_by_username(db, username="testuser")
        
        # Assert
        assert result is not None
        assert result.username == "testuser"
        assert result.email == "test@example.com"

    def test_get_user_by_username_not_found(self, db: Session):
        """存在しないユーザー名でのユーザー取得テスト"""
        # Act
        result = crud_user.get_user_by_username(db, username="notfound")
        
        # Assert
        assert result is None

    def test_get_users_empty(self, db: Session):
        """ユーザーリストの取得（空の場合）"""
        # Act
        result = crud_user.get_users(db)
        
        # Assert
        assert result == []

    def test_get_users_with_data(self, db: Session):
        """ユーザーリストの取得（データあり）"""
        # Arrange
        user1 = User(username="user1", email="user1@example.com")
        user2 = User(username="user2", email="user2@example.com")
        db.add_all([user1, user2])
        db.commit()
        
        # Act
        result = crud_user.get_users(db)
        
        # Assert
        assert len(result) == 2
        assert result[0].username == "user1"
        assert result[1].username == "user2"

    def test_get_users_with_pagination(self, db: Session):
        """ページネーション付きユーザーリストの取得"""
        # Arrange
        for i in range(5):
            user = User(username=f"user{i}", email=f"user{i}@example.com")
            db.add(user)
        db.commit()
        
        # Act
        result = crud_user.get_users(db, skip=1, limit=2)
        
        # Assert
        assert len(result) == 2
        assert result[0].username == "user1"
        assert result[1].username == "user2"

    def test_create_user(self, db: Session):
        """ユーザーの作成テスト"""
        # Arrange
        user_data = UserCreate(
            username="newuser",
            email="newuser@example.com"
        )
        
        # Act
        result = crud_user.create_user(db, user=user_data)
        
        # Assert
        assert result.id is not None
        assert result.username == "newuser"
        assert result.email == "newuser@example.com"
        assert result.created_at is not None

    def test_create_user_duplicate_email(self, db: Session):
        """重複するメールアドレスでのユーザー作成テスト"""
        # Arrange
        existing_user = User(username="existing", email="duplicate@example.com")
        db.add(existing_user)
        db.commit()
        
        user_data = UserCreate(
            username="newuser",
            email="duplicate@example.com"
        )
        
        # Act & Assert
        # 実際の実装では、重複チェックを行うか、データベースの制約でエラーになる
        # ここでは、create_userが既存のユーザーをチェックすることを想定
        result = crud_user.create_user(db, user=user_data)
        assert result is None  # または例外が発生することを期待

    def test_create_user_duplicate_username(self, db: Session):
        """重複するユーザー名でのユーザー作成テスト"""
        # Arrange
        existing_user = User(username="duplicate", email="existing@example.com")
        db.add(existing_user)
        db.commit()
        
        user_data = UserCreate(
            username="duplicate",
            email="newuser@example.com"
        )
        
        # Act & Assert
        result = crud_user.create_user(db, user=user_data)
        assert result is None  # または例外が発生することを期待 