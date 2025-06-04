"""
Tests for task API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate


class TestTaskAPI:
    """Test cases for task API endpoints"""

    def test_create_task(self, client: TestClient, db: Session):
        """Test creating a new task"""
        # Arrange - Create project and user first
        project = Project(name="Test Project", description="Test Description")
        user = User(username="testuser", email="test@example.com")
        db.add(project)
        db.add(user)
        db.commit()
        db.refresh(project)
        db.refresh(user)
        
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending",
            "project_id": project.id,
            "assignee_id": user.id
        }
        
        # Act
        response = client.post("/tasks/", json=task_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert data["project_id"] == task_data["project_id"]
        assert data["assignee_id"] == task_data["assignee_id"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_tasks(self, client: TestClient, db: Session):
        """Test getting all tasks"""
        # Arrange - Create project, user and tasks
        project = Project(name="Test Project", description="Test Description")
        user = User(username="testuser", email="test@example.com")
        db.add(project)
        db.add(user)
        db.commit()
        db.refresh(project)
        db.refresh(user)
        
        task1 = Task(
            title="Task 1",
            description="Description 1",
            status="pending",
            project_id=project.id,
            assignee_id=user.id
        )
        task2 = Task(
            title="Task 2",
            description="Description 2",
            status="in_progress",
            project_id=project.id,
            assignee_id=user.id
        )
        db.add(task1)
        db.add(task2)
        db.commit()
        
        # Act
        response = client.get("/tasks/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        task_titles = [t["title"] for t in data]
        assert "Task 1" in task_titles
        assert "Task 2" in task_titles

    def test_get_task_by_id(self, client: TestClient, db: Session):
        """Test getting a specific task by ID"""
        # Arrange
        project = Project(name="Test Project", description="Test Description")
        user = User(username="testuser", email="test@example.com")
        db.add(project)
        db.add(user)
        db.commit()
        db.refresh(project)
        db.refresh(user)
        
        task = Task(
            title="Test Task",
            description="Test Description",
            status="pending",
            project_id=project.id,
            assignee_id=user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # Act
        response = client.get(f"/tasks/{task.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task.id
        assert data["title"] == task.title
        assert data["description"] == task.description
        assert data["status"] == task.status

    def test_get_task_not_found(self, client: TestClient):
        """Test getting a non-existent task"""
        # Act
        response = client.get("/tasks/999999")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_update_task(self, client: TestClient, db: Session):
        """Test updating a task"""
        # Arrange
        project = Project(name="Test Project", description="Test Description")
        user = User(username="testuser", email="test@example.com")
        db.add(project)
        db.add(user)
        db.commit()
        db.refresh(project)
        db.refresh(user)
        
        task = Task(
            title="Original Title",
            description="Original Description",
            status="pending",
            project_id=project.id,
            assignee_id=user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "status": "completed"
        }
        
        # Act
        response = client.put(f"/tasks/{task.id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task.id
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["status"] == update_data["status"]

    def test_update_task_not_found(self, client: TestClient):
        """Test updating a non-existent task"""
        # Arrange
        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "status": "completed"
        }
        
        # Act
        response = client.put("/tasks/999999", json=update_data)
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_delete_task(self, client: TestClient, db: Session):
        """Test deleting a task"""
        # Arrange
        project = Project(name="Test Project", description="Test Description")
        user = User(username="testuser", email="test@example.com")
        db.add(project)
        db.add(user)
        db.commit()
        db.refresh(project)
        db.refresh(user)
        
        task = Task(
            title="To Delete",
            description="Will be deleted",
            status="pending",
            project_id=project.id,
            assignee_id=user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # Act
        response = client.delete(f"/tasks/{task.id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verify task is deleted
        deleted_task = db.query(Task).filter(Task.id == task.id).first()
        assert deleted_task is None

    def test_delete_task_not_found(self, client: TestClient):
        """Test deleting a non-existent task"""
        # Act
        response = client.delete("/tasks/999999")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_create_task_invalid_data(self, client: TestClient):
        """Test creating a task with invalid data"""
        # Arrange - Missing required field
        task_data = {
            "description": "Missing title field",
            "status": "pending"
        }
        
        # Act
        response = client.post("/tasks/", json=task_data)
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity

    def test_update_task_partial(self, client: TestClient, db: Session):
        """Test partial update of a task"""
        # Arrange
        project = Project(name="Test Project", description="Test Description")
        user = User(username="testuser", email="test@example.com")
        db.add(project)
        db.add(user)
        db.commit()
        db.refresh(project)
        db.refresh(user)
        
        task = Task(
            title="Original Title",
            description="Original Description",
            status="pending",
            project_id=project.id,
            assignee_id=user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        update_data = {
            "status": "in_progress"
            # title and description are not provided
        }
        
        # Act
        response = client.put(f"/tasks/{task.id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == update_data["status"]
        assert data["title"] == task.title  # Should remain unchanged
        assert data["description"] == task.description  # Should remain unchanged

    def test_get_tasks_by_project(self, client: TestClient, db: Session):
        """Test getting tasks filtered by project"""
        # Arrange - Create two projects with tasks
        project1 = Project(name="Project 1", description="Description 1")
        project2 = Project(name="Project 2", description="Description 2")
        user = User(username="testuser", email="test@example.com")
        db.add(project1)
        db.add(project2)
        db.add(user)
        db.commit()
        db.refresh(project1)
        db.refresh(project2)
        db.refresh(user)
        
        task1 = Task(
            title="Task for Project 1",
            description="Description",
            status="pending",
            project_id=project1.id,
            assignee_id=user.id
        )
        task2 = Task(
            title="Task for Project 2",
            description="Description",
            status="pending",
            project_id=project2.id,
            assignee_id=user.id
        )
        db.add(task1)
        db.add(task2)
        db.commit()
        
        # Act
        response = client.get(f"/tasks/?project_id={project1.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["project_id"] == project1.id
        assert data[0]["title"] == "Task for Project 1"

    def test_get_tasks_by_assignee(self, client: TestClient, db: Session):
        """Test getting tasks filtered by assignee"""
        # Arrange - Create two users with tasks
        project = Project(name="Test Project", description="Test Description")
        user1 = User(username="user1", email="user1@example.com")
        user2 = User(username="user2", email="user2@example.com")
        db.add(project)
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(project)
        db.refresh(user1)
        db.refresh(user2)
        
        task1 = Task(
            title="Task for User 1",
            description="Description",
            status="pending",
            project_id=project.id,
            assignee_id=user1.id
        )
        task2 = Task(
            title="Task for User 2",
            description="Description",
            status="pending",
            project_id=project.id,
            assignee_id=user2.id
        )
        db.add(task1)
        db.add(task2)
        db.commit()
        
        # Act
        response = client.get(f"/tasks/?assignee_id={user1.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["assignee_id"] == user1.id
        assert data[0]["title"] == "Task for User 1" 