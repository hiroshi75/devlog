"""
Taskスキーマのテスト

TaskBase, TaskCreate, TaskUpdate, Taskスキーマの
バリデーションと動作をテストします。
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.task import TaskBase, TaskCreate, TaskUpdate, Task, TaskStatus


class TestTaskStatus:
    """TaskStatus列挙型のテスト"""
    
    def test_task_status_values(self):
        """タスクステータスの値を確認"""
        assert TaskStatus.PENDING == "pending"
        assert TaskStatus.IN_PROGRESS == "in_progress"
        assert TaskStatus.COMPLETED == "completed"
        assert TaskStatus.CANCELLED == "cancelled"


class TestTaskBase:
    """TaskBaseスキーマのテスト"""
    
    def test_valid_task_base(self):
        """有効なTaskBaseの作成"""
        task = TaskBase(
            title="Test Task",
            description="This is a test task",
            status=TaskStatus.PENDING,
            project_id=1,
            assignee_id=1
        )
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.status == TaskStatus.PENDING
        assert task.project_id == 1
        assert task.assignee_id == 1
    
    def test_task_base_without_optional_fields(self):
        """オプションフィールドなしのTaskBase"""
        task = TaskBase(
            title="Test Task",
            status=TaskStatus.PENDING,
            project_id=1
        )
        assert task.title == "Test Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING
        assert task.project_id == 1
        assert task.assignee_id is None
    
    def test_task_base_empty_title(self):
        """空のタイトルでエラー"""
        with pytest.raises(ValidationError):
            TaskBase(
                title="",
                status=TaskStatus.PENDING,
                project_id=1
            )
    
    def test_task_base_invalid_status(self):
        """無効なステータスでエラー"""
        with pytest.raises(ValidationError):
            TaskBase(
                title="Test Task",
                status="invalid_status",
                project_id=1
            )
    
    def test_task_base_missing_required_fields(self):
        """必須フィールドなしでエラー"""
        with pytest.raises(ValidationError):
            TaskBase(title="Test Task")


class TestTaskCreate:
    """TaskCreateスキーマのテスト"""
    
    def test_valid_task_create(self):
        """有効なTaskCreateの作成"""
        task = TaskCreate(
            title="New Task",
            description="Creating a new task",
            status=TaskStatus.PENDING,
            project_id=1,
            assignee_id=2
        )
        assert task.title == "New Task"
        assert task.description == "Creating a new task"
        assert task.status == TaskStatus.PENDING
        assert task.project_id == 1
        assert task.assignee_id == 2
    
    def test_task_create_inherits_from_base(self):
        """TaskBaseを継承していることを確認"""
        assert issubclass(TaskCreate, TaskBase)


class TestTaskUpdate:
    """TaskUpdateスキーマのテスト"""
    
    def test_update_all_fields(self):
        """全フィールドの更新"""
        update = TaskUpdate(
            title="Updated Task",
            description="Updated description",
            status=TaskStatus.COMPLETED,
            assignee_id=3
        )
        assert update.title == "Updated Task"
        assert update.description == "Updated description"
        assert update.status == TaskStatus.COMPLETED
        assert update.assignee_id == 3
    
    def test_update_status_only(self):
        """ステータスのみ更新"""
        update = TaskUpdate(status=TaskStatus.IN_PROGRESS)
        assert update.title is None
        assert update.description is None
        assert update.status == TaskStatus.IN_PROGRESS
        assert update.assignee_id is None
    
    def test_empty_update(self):
        """空の更新（全フィールドがオプション）"""
        update = TaskUpdate()
        assert update.title is None
        assert update.description is None
        assert update.status is None
        assert update.assignee_id is None


class TestTask:
    """Taskレスポンススキーマのテスト"""
    
    def test_valid_task_response(self):
        """有効なTaskレスポンスの作成"""
        now = datetime.now()
        task = Task(
            id=1,
            title="Test Task",
            description="Test description",
            status=TaskStatus.PENDING,
            project_id=1,
            assignee_id=2,
            created_at=now,
            updated_at=now
        )
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.PENDING
        assert task.project_id == 1
        assert task.assignee_id == 2
        assert task.created_at == now
        assert task.updated_at == now
    
    def test_task_inherits_from_base(self):
        """TaskBaseを継承していることを確認"""
        assert issubclass(Task, TaskBase)
    
    def test_task_from_orm_mode(self):
        """ORMモードが有効であることを確認"""
        assert hasattr(Task, 'model_config')
        assert Task.model_config.get('from_attributes', False) is True 