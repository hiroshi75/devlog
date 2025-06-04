"""
メッセージCRUD操作のテスト
"""
import pytest
from sqlalchemy.orm import Session
from app.crud import message as crud_message
from app.schemas.message import MessageCreate
from app.models.message import Message
from app.models.project import Project
from app.models.task import Task
from app.models.user import User


class TestMessageCRUD:
    """メッセージCRUD操作のテストクラス"""

    @pytest.fixture
    def test_user(self, db: Session) -> User:
        """テスト用のユーザーを作成"""
        user = User(username="testuser", email="test@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @pytest.fixture
    def test_project(self, db: Session) -> Project:
        """テスト用のプロジェクトを作成"""
        project = Project(name="Test Project", description="Test Description")
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @pytest.fixture
    def test_task(self, db: Session, test_project: Project) -> Task:
        """テスト用のタスクを作成"""
        task = Task(
            title="Test Task",
            description="Test Description",
            status="pending",
            project_id=test_project.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def test_get_message_by_id(self, db: Session, test_user: User, test_project: Project):
        """IDによるメッセージ取得のテスト"""
        # Arrange
        message = Message(
            content="Test message",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        
        # Act
        result = crud_message.get_message(db, message_id=message.id)
        
        # Assert
        assert result is not None
        assert result.id == message.id
        assert result.content == "Test message"
        assert result.message_type == "comment"
        assert result.user_id == test_user.id
        assert result.project_id == test_project.id

    def test_get_message_not_found(self, db: Session):
        """存在しないメッセージの取得テスト"""
        # Act
        result = crud_message.get_message(db, message_id=999)
        
        # Assert
        assert result is None

    def test_get_messages_empty(self, db: Session):
        """メッセージリストの取得（空の場合）"""
        # Act
        result = crud_message.get_messages(db)
        
        # Assert
        assert result == []

    def test_get_messages_with_data(self, db: Session, test_user: User, test_project: Project):
        """メッセージリストの取得（データあり）"""
        # Arrange
        message1 = Message(
            content="Message 1",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        message2 = Message(
            content="Message 2",
            message_type="status_update",
            user_id=test_user.id,
            project_id=test_project.id
        )
        db.add_all([message1, message2])
        db.commit()
        
        # Act
        result = crud_message.get_messages(db)
        
        # Assert
        assert len(result) == 2
        assert result[0].content == "Message 1"
        assert result[1].content == "Message 2"

    def test_get_messages_by_project(self, db: Session, test_user: User, test_project: Project):
        """プロジェクトIDによるメッセージの取得"""
        # Arrange
        project2 = Project(name="Project 2", description="Description 2")
        db.add(project2)
        db.commit()
        db.refresh(project2)
        
        message1 = Message(
            content="Message 1",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        message2 = Message(
            content="Message 2",
            message_type="comment",
            user_id=test_user.id,
            project_id=project2.id
        )
        db.add_all([message1, message2])
        db.commit()
        
        # Act
        result = crud_message.get_messages(db, project_id=test_project.id)
        
        # Assert
        assert len(result) == 1
        assert result[0].content == "Message 1"
        assert result[0].project_id == test_project.id

    def test_get_messages_by_task(self, db: Session, test_user: User, test_task: Task):
        """タスクIDによるメッセージの取得"""
        # Arrange
        message1 = Message(
            content="Task Message",
            message_type="comment",
            user_id=test_user.id,
            task_id=test_task.id,
            project_id=test_task.project_id
        )
        message2 = Message(
            content="Other Message",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_task.project_id
        )
        db.add_all([message1, message2])
        db.commit()
        
        # Act
        result = crud_message.get_messages(db, task_id=test_task.id)
        
        # Assert
        assert len(result) == 1
        assert result[0].content == "Task Message"
        assert result[0].task_id == test_task.id

    def test_get_messages_by_user(self, db: Session, test_user: User, test_project: Project):
        """ユーザーIDによるメッセージの取得"""
        # Arrange
        user2 = User(username="user2", email="user2@example.com")
        db.add(user2)
        db.commit()
        db.refresh(user2)
        
        message1 = Message(
            content="User1 Message",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        message2 = Message(
            content="User2 Message",
            message_type="comment",
            user_id=user2.id,
            project_id=test_project.id
        )
        db.add_all([message1, message2])
        db.commit()
        
        # Act
        result = crud_message.get_messages(db, user_id=test_user.id)
        
        # Assert
        assert len(result) == 1
        assert result[0].content == "User1 Message"
        assert result[0].user_id == test_user.id

    def test_get_messages_by_type(self, db: Session, test_user: User, test_project: Project):
        """メッセージタイプによるメッセージの取得"""
        # Arrange
        message1 = Message(
            content="Comment",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        message2 = Message(
            content="Status Update",
            message_type="status_update",
            user_id=test_user.id,
            project_id=test_project.id
        )
        db.add_all([message1, message2])
        db.commit()
        
        # Act
        result = crud_message.get_messages(db, message_type="comment")
        
        # Assert
        assert len(result) == 1
        assert result[0].content == "Comment"
        assert result[0].message_type == "comment"

    def test_create_message_for_project(self, db: Session, test_user: User, test_project: Project):
        """プロジェクトへのメッセージ作成テスト"""
        # Arrange
        message_data = MessageCreate(
            content="New project message",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        
        # Act
        result = crud_message.create_message(db, message=message_data)
        
        # Assert
        assert result.id is not None
        assert result.content == "New project message"
        assert result.message_type == "comment"
        assert result.user_id == test_user.id
        assert result.project_id == test_project.id
        assert result.task_id is None
        assert result.parent_id is None
        assert result.created_at is not None

    def test_create_message_for_task(self, db: Session, test_user: User, test_task: Task):
        """タスクへのメッセージ作成テスト"""
        # Arrange
        message_data = MessageCreate(
            content="New task message",
            message_type="status_update",
            user_id=test_user.id,
            task_id=test_task.id,
            project_id=test_task.project_id
        )
        
        # Act
        result = crud_message.create_message(db, message=message_data)
        
        # Assert
        assert result.id is not None
        assert result.content == "New task message"
        assert result.message_type == "status_update"
        assert result.user_id == test_user.id
        assert result.task_id == test_task.id
        assert result.project_id == test_task.project_id

    def test_create_reply_message(self, db: Session, test_user: User, test_project: Project):
        """返信メッセージの作成テスト"""
        # Arrange
        parent_message = Message(
            content="Parent message",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id
        )
        db.add(parent_message)
        db.commit()
        db.refresh(parent_message)
        
        message_data = MessageCreate(
            content="Reply message",
            message_type="comment",
            user_id=test_user.id,
            project_id=test_project.id,
            parent_id=parent_message.id
        )
        
        # Act
        result = crud_message.create_message(db, message=message_data)
        
        # Assert
        assert result.id is not None
        assert result.content == "Reply message"
        assert result.parent_id == parent_message.id

    def test_get_messages_with_pagination(self, db: Session, test_user: User, test_project: Project):
        """ページネーション付きメッセージリストの取得"""
        # Arrange
        for i in range(5):
            message = Message(
                content=f"Message {i}",
                message_type="comment",
                user_id=test_user.id,
                project_id=test_project.id
            )
            db.add(message)
        db.commit()
        
        # Act
        result = crud_message.get_messages(db, skip=1, limit=2)
        
        # Assert
        assert len(result) == 2
        assert result[0].content == "Message 1"
        assert result[1].content == "Message 2" 