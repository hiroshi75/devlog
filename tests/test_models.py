"""
モデルのテスト
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.models.message import Message


class TestProjectModel:
    """Projectモデルのテストクラス"""
    
    @pytest.fixture
    def db_session(self):
        """テスト用のデータベースセッションを作成"""
        # SQLiteのメモリDBを使用
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
    
    def test_create_project_success(self, db_session):
        """プロジェクトの作成が成功することを確認"""
        # Arrange
        project_data = {
            "name": "テストプロジェクト",
            "description": "これはテスト用のプロジェクトです"
        }
        
        # Act
        project = Project(**project_data)
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        
        # Assert
        assert project.id is not None
        assert project.name == "テストプロジェクト"
        assert project.description == "これはテスト用のプロジェクトです"
        assert isinstance(project.created_at, datetime)
        assert isinstance(project.updated_at, datetime)
    
    def test_project_required_fields(self, db_session):
        """必須フィールドが設定されていることを確認"""
        # Arrange & Act
        project = Project(name="必須フィールドテスト")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        
        # Assert
        assert project.name == "必須フィールドテスト"
        assert project.description is None  # descriptionはオプション
        assert project.created_at is not None
        assert project.updated_at is not None
    
    def test_project_update(self, db_session):
        """プロジェクトの更新が正しく動作することを確認"""
        # Arrange
        project = Project(name="更新前", description="更新前の説明")
        db_session.add(project)
        db_session.commit()
        original_created_at = project.created_at
        
        # Act
        project.name = "更新後"
        project.description = "更新後の説明"
        db_session.commit()
        db_session.refresh(project)
        
        # Assert
        assert project.name == "更新後"
        assert project.description == "更新後の説明"
        assert project.created_at == original_created_at  # created_atは変更されない
        assert project.updated_at > original_created_at  # updated_atは更新される
    
    def test_project_str_representation(self, db_session):
        """プロジェクトの文字列表現が正しいことを確認"""
        # Arrange & Act
        project = Project(name="表示テスト", description="説明文")
        
        # Assert
        assert str(project) == "<Project(name='表示テスト')>"
        assert repr(project) == "<Project(name='表示テスト')>"


class TestTaskModel:
    """Taskモデルのテストクラス"""
    
    @pytest.fixture
    def db_session(self):
        """テスト用のデータベースセッションを作成"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
    
    @pytest.fixture
    def test_project(self, db_session):
        """テスト用のプロジェクトを作成"""
        project = Project(name="テストプロジェクト")
        db_session.add(project)
        db_session.commit()
        return project
    
    def test_create_task_success(self, db_session, test_project):
        """タスクの作成が成功することを確認"""
        # Arrange
        task_data = {
            "title": "テストタスク",
            "description": "これはテスト用のタスクです",
            "status": "pending",
            "project_id": test_project.id,
            "assignee_id": 1
        }
        
        # Act
        task = Task(**task_data)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Assert
        assert task.id is not None
        assert task.title == "テストタスク"
        assert task.description == "これはテスト用のタスクです"
        assert task.status == "pending"
        assert task.project_id == test_project.id
        assert task.assignee_id == 1
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)
    
    def test_task_required_fields(self, db_session, test_project):
        """必須フィールドが設定されていることを確認"""
        # Arrange & Act
        task = Task(
            title="必須フィールドテスト",
            status="pending",
            project_id=test_project.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Assert
        assert task.title == "必須フィールドテスト"
        assert task.status == "pending"
        assert task.project_id == test_project.id
        assert task.description is None  # descriptionはオプション
        assert task.assignee_id is None  # assignee_idはオプション
    
    def test_task_status_values(self, db_session, test_project):
        """タスクのステータス値が正しく設定できることを確認"""
        # Arrange
        statuses = ["pending", "in_progress", "completed", "cancelled"]
        
        for status in statuses:
            # Act
            task = Task(
                title=f"ステータステスト_{status}",
                status=status,
                project_id=test_project.id
            )
            db_session.add(task)
            db_session.commit()
            
            # Assert
            assert task.status == status
    
    def test_task_project_relationship(self, db_session, test_project):
        """タスクとプロジェクトの関係が正しく設定されることを確認"""
        # Arrange & Act
        task = Task(
            title="関係テスト",
            status="pending",
            project_id=test_project.id
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Assert
        assert task.project_id == test_project.id
        assert task.project.name == "テストプロジェクト"
    
    def test_task_str_representation(self, db_session, test_project):
        """タスクの文字列表現が正しいことを確認"""
        # Arrange & Act
        task = Task(
            title="表示テスト",
            status="pending",
            project_id=test_project.id
        )
        
        # Assert
        assert str(task) == "<Task(title='表示テスト', status='pending')>"
        assert repr(task) == "<Task(title='表示テスト', status='pending')>"


class TestUserModel:
    """Userモデルのテストクラス"""
    
    @pytest.fixture
    def db_session(self):
        """テスト用のデータベースセッションを作成"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
    
    def test_create_user_success(self, db_session):
        """ユーザーの作成が成功することを確認"""
        # Arrange
        user_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        
        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Assert
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert isinstance(user.created_at, datetime)
    
    def test_user_unique_username(self, db_session):
        """ユーザー名が一意であることを確認"""
        # Arrange
        user1 = User(username="uniqueuser", email="user1@example.com")
        user2 = User(username="uniqueuser", email="user2@example.com")
        
        # Act & Assert
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_user_unique_email(self, db_session):
        """メールアドレスが一意であることを確認"""
        # Arrange
        user1 = User(username="user1", email="same@example.com")
        user2 = User(username="user2", email="same@example.com")
        
        # Act & Assert
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_user_str_representation(self, db_session):
        """ユーザーの文字列表現が正しいことを確認"""
        # Arrange & Act
        user = User(username="displaytest", email="display@example.com")
        
        # Assert
        assert str(user) == "<User(username='displaytest', email='display@example.com')>"
        assert repr(user) == "<User(username='displaytest', email='display@example.com')>"


class TestMessageModel:
    """Messageモデルのテストクラス"""
    
    @pytest.fixture
    def db_session(self):
        """テスト用のデータベースセッションを作成"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
    
    @pytest.fixture
    def test_user(self, db_session):
        """テスト用のユーザーを作成"""
        user = User(username="testuser", email="test@example.com")
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def test_project(self, db_session):
        """テスト用のプロジェクトを作成"""
        project = Project(name="テストプロジェクト")
        db_session.add(project)
        db_session.commit()
        return project
    
    @pytest.fixture
    def test_task(self, db_session, test_project, test_user):
        """テスト用のタスクを作成"""
        task = Task(
            title="テストタスク",
            status="pending",
            project_id=test_project.id,
            assignee_id=test_user.id
        )
        db_session.add(task)
        db_session.commit()
        return task
    
    def test_create_message_success(self, db_session, test_user, test_project):
        """メッセージの作成が成功することを確認"""
        # Arrange
        message_data = {
            "content": "これはテストメッセージです",
            "message_type": "comment",
            "user_id": test_user.id,
            "project_id": test_project.id
        }
        
        # Act
        message = Message(**message_data)
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        
        # Assert
        assert message.id is not None
        assert message.content == "これはテストメッセージです"
        assert message.message_type == "comment"
        assert message.user_id == test_user.id
        assert message.project_id == test_project.id
        assert message.task_id is None
        assert message.parent_id is None
        assert isinstance(message.created_at, datetime)
    
    def test_message_with_task(self, db_session, test_user, test_task):
        """タスクに関連するメッセージが作成できることを確認"""
        # Arrange & Act
        message = Message(
            content="タスクに関するコメント",
            message_type="task_update",
            user_id=test_user.id,
            task_id=test_task.id,
            project_id=test_task.project_id
        )
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        
        # Assert
        assert message.task_id == test_task.id
        assert message.project_id == test_task.project_id
    
    def test_message_reply(self, db_session, test_user, test_project):
        """返信メッセージが作成できることを確認"""
        # Arrange
        parent_message = Message(
            content="親メッセージ",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        db_session.add(parent_message)
        db_session.commit()
        
        # Act
        reply_message = Message(
            content="返信メッセージ",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id,
            parent_id=parent_message.id
        )
        db_session.add(reply_message)
        db_session.commit()
        db_session.refresh(reply_message)
        
        # Assert
        assert reply_message.parent_id == parent_message.id
        assert reply_message.parent.content == "親メッセージ"
    
    def test_message_types(self, db_session, test_user, test_project):
        """様々なメッセージタイプが設定できることを確認"""
        # Arrange
        message_types = ["comment", "task_update", "status_change", "announcement"]
        
        for msg_type in message_types:
            # Act
            message = Message(
                content=f"{msg_type}のテスト",
                message_type=msg_type,
                user_id=test_user.id,
                project_id=test_project.id
            )
            db_session.add(message)
            db_session.commit()
            
            # Assert
            assert message.message_type == msg_type
    
    def test_message_relationships(self, db_session, test_user, test_project, test_task):
        """メッセージのリレーションシップが正しく動作することを確認"""
        # Arrange & Act
        message = Message(
            content="関係テスト",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id,
            task_id=test_task.id
        )
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        
        # Assert
        assert message.user.username == "testuser"
        assert message.project.name == "テストプロジェクト"
        assert message.task.title == "テストタスク"
    
    def test_message_str_representation(self, db_session, test_user, test_project):
        """メッセージの文字列表現が正しいことを確認"""
        # Arrange & Act
        message = Message(
            content="表示テスト",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        
        # Assert
        expected = "<Message(type='comment', user_id=1, project_id=1)>"
        assert str(message) == expected
        assert repr(message) == expected 