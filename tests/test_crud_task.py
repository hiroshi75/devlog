"""
タスクCRUD操作のテスト
"""
import pytest
from sqlalchemy.orm import Session
from app.crud import task as crud_task
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task
from app.models.project import Project
from app.models.user import User


class TestTaskCRUD:
    """タスクCRUD操作のテストクラス"""

    @pytest.fixture
    def test_project(self, db: Session) -> Project:
        """テスト用のプロジェクトを作成"""
        project = Project(name="Test Project", description="Test Description")
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @pytest.fixture
    def test_user(self, db: Session) -> User:
        """テスト用のユーザーを作成"""
        user = User(username="testuser", email="test@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def test_get_task_by_id(self, db: Session, test_project: Project, test_user: User):
        """IDによるタスク取得のテスト"""
        # Arrange
        task = Task(
            title="Test Task",
            description="Test Description",
            status="pending",
            project_id=test_project.id,
            assignee_id=test_user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # Act
        result = crud_task.get_task(db, task_id=task.id)
        
        # Assert
        assert result is not None
        assert result.id == task.id
        assert result.title == "Test Task"
        assert result.description == "Test Description"
        assert result.status == "pending"
        assert result.project_id == test_project.id
        assert result.assignee_id == test_user.id

    def test_get_task_not_found(self, db: Session):
        """存在しないタスクの取得テスト"""
        # Act
        result = crud_task.get_task(db, task_id=999)
        
        # Assert
        assert result is None

    def test_get_tasks_empty(self, db: Session):
        """タスクリストの取得（空の場合）"""
        # Act
        result = crud_task.get_tasks(db)
        
        # Assert
        assert result == []

    def test_get_tasks_with_data(self, db: Session, test_project: Project):
        """タスクリストの取得（データあり）"""
        # Arrange
        task1 = Task(
            title="Task 1",
            description="Description 1",
            status="pending",
            project_id=test_project.id
        )
        task2 = Task(
            title="Task 2",
            description="Description 2",
            status="in_progress",
            project_id=test_project.id
        )
        db.add_all([task1, task2])
        db.commit()
        
        # Act
        result = crud_task.get_tasks(db)
        
        # Assert
        assert len(result) == 2
        assert result[0].title == "Task 1"
        assert result[1].title == "Task 2"

    def test_get_tasks_with_pagination(self, db: Session, test_project: Project):
        """ページネーション付きタスクリストの取得"""
        # Arrange
        for i in range(5):
            task = Task(
                title=f"Task {i}",
                description=f"Description {i}",
                status="pending",
                project_id=test_project.id
            )
            db.add(task)
        db.commit()
        
        # Act
        result = crud_task.get_tasks(db, skip=1, limit=2)
        
        # Assert
        assert len(result) == 2
        assert result[0].title == "Task 1"
        assert result[1].title == "Task 2"

    def test_get_tasks_by_project(self, db: Session, test_project: Project):
        """プロジェクトIDによるタスクの取得"""
        # Arrange
        project2 = Project(name="Project 2", description="Description 2")
        db.add(project2)
        db.commit()
        db.refresh(project2)
        
        task1 = Task(
            title="Task 1",
            description="Description 1",
            status="pending",
            project_id=test_project.id
        )
        task2 = Task(
            title="Task 2",
            description="Description 2",
            status="pending",
            project_id=project2.id
        )
        db.add_all([task1, task2])
        db.commit()
        
        # Act
        result = crud_task.get_tasks(db, project_id=test_project.id)
        
        # Assert
        assert len(result) == 1
        assert result[0].title == "Task 1"
        assert result[0].project_id == test_project.id

    def test_get_tasks_by_status(self, db: Session, test_project: Project):
        """ステータスによるタスクの取得"""
        # Arrange
        task1 = Task(
            title="Task 1",
            description="Description 1",
            status="pending",
            project_id=test_project.id
        )
        task2 = Task(
            title="Task 2",
            description="Description 2",
            status="completed",
            project_id=test_project.id
        )
        db.add_all([task1, task2])
        db.commit()
        
        # Act
        result = crud_task.get_tasks(db, status="pending")
        
        # Assert
        assert len(result) == 1
        assert result[0].title == "Task 1"
        assert result[0].status == "pending"

    def test_create_task(self, db: Session, test_project: Project, test_user: User):
        """タスクの作成テスト"""
        # Arrange
        task_data = TaskCreate(
            title="New Task",
            description="New Description",
            status="pending",
            project_id=test_project.id,
            assignee_id=test_user.id
        )
        
        # Act
        result = crud_task.create_task(db, task=task_data)
        
        # Assert
        assert result.id is not None
        assert result.title == "New Task"
        assert result.description == "New Description"
        assert result.status == "pending"
        assert result.project_id == test_project.id
        assert result.assignee_id == test_user.id
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_update_task(self, db: Session, test_project: Project):
        """タスクの更新テスト"""
        # Arrange
        task = Task(
            title="Original Title",
            description="Original Description",
            status="pending",
            project_id=test_project.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        update_data = TaskUpdate(
            title="Updated Title",
            description="Updated Description",
            status="in_progress"
        )
        
        # Act
        result = crud_task.update_task(db, task_id=task.id, task=update_data)
        
        # Assert
        assert result is not None
        assert result.title == "Updated Title"
        assert result.description == "Updated Description"
        assert result.status == "in_progress"
        assert result.updated_at > task.created_at

    def test_update_task_partial(self, db: Session, test_project: Project):
        """タスクの部分更新テスト"""
        # Arrange
        task = Task(
            title="Original Title",
            description="Original Description",
            status="pending",
            project_id=test_project.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        update_data = TaskUpdate(status="completed")
        
        # Act
        result = crud_task.update_task(db, task_id=task.id, task=update_data)
        
        # Assert
        assert result is not None
        assert result.title == "Original Title"  # 変更されていない
        assert result.description == "Original Description"  # 変更されていない
        assert result.status == "completed"

    def test_update_task_not_found(self, db: Session):
        """存在しないタスクの更新テスト"""
        # Arrange
        update_data = TaskUpdate(title="Updated Title")
        
        # Act
        result = crud_task.update_task(db, task_id=999, task=update_data)
        
        # Assert
        assert result is None

    def test_delete_task(self, db: Session, test_project: Project):
        """タスクの削除テスト"""
        # Arrange
        task = Task(
            title="To Delete",
            description="Will be deleted",
            status="pending",
            project_id=test_project.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        task_id = task.id
        
        # Act
        result = crud_task.delete_task(db, task_id=task_id)
        
        # Assert
        assert result is True
        assert crud_task.get_task(db, task_id=task_id) is None

    def test_delete_task_not_found(self, db: Session):
        """存在しないタスクの削除テスト"""
        # Act
        result = crud_task.delete_task(db, task_id=999)
        
        # Assert
        assert result is False 