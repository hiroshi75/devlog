"""
Tests for message API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.message import Message
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.message import MessageCreate


class TestMessageAPI:
    """Test cases for message API endpoints"""

    def test_create_message(self, client: TestClient, db: Session):
        """Test creating a new message"""
        # Arrange - Create user, project, and task first
        user = User(username="testuser", email="test@example.com")
        project = Project(name="Test Project", description="Test Description")
        db.add(user)
        db.add(project)
        db.commit()
        db.refresh(user)
        db.refresh(project)
        
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
        
        message_data = {
            "content": "This is a test message",
            "message_type": "comment",
            "user_id": user.id,
            "task_id": task.id,
            "project_id": project.id
        }
        
        # Act
        response = client.post("/messages/", json=message_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == message_data["content"]
        assert data["message_type"] == message_data["message_type"]
        assert data["user_id"] == message_data["user_id"]
        assert data["task_id"] == message_data["task_id"]
        assert data["project_id"] == message_data["project_id"]
        assert "id" in data
        assert "created_at" in data

    def test_get_messages(self, client: TestClient, db: Session):
        """Test getting all messages"""
        # Arrange - Create user, project, and messages
        user = User(username="testuser", email="test@example.com")
        project = Project(name="Test Project", description="Test Description")
        db.add(user)
        db.add(project)
        db.commit()
        db.refresh(user)
        db.refresh(project)
        
        message1 = Message(
            content="Message 1",
            message_type="comment",
            user_id=user.id,
            project_id=project.id
        )
        message2 = Message(
            content="Message 2",
            message_type="status_update",
            user_id=user.id,
            project_id=project.id
        )
        db.add(message1)
        db.add(message2)
        db.commit()
        
        # Act
        response = client.get("/messages/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        contents = [m["content"] for m in data]
        assert "Message 1" in contents
        assert "Message 2" in contents

    def test_get_message_by_id(self, client: TestClient, db: Session):
        """Test getting a specific message by ID"""
        # Arrange
        user = User(username="testuser", email="test@example.com")
        project = Project(name="Test Project", description="Test Description")
        db.add(user)
        db.add(project)
        db.commit()
        db.refresh(user)
        db.refresh(project)
        
        message = Message(
            content="Test Message",
            message_type="comment",
            user_id=user.id,
            project_id=project.id
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        
        # Act
        response = client.get(f"/messages/{message.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == message.id
        assert data["content"] == message.content
        assert data["message_type"] == message.message_type

    def test_get_message_not_found(self, client: TestClient):
        """Test getting a non-existent message"""
        # Act
        response = client.get("/messages/999999")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Message not found"

    def test_create_message_invalid_data(self, client: TestClient):
        """Test creating a message with invalid data"""
        # Arrange - Missing required field
        message_data = {
            "message_type": "comment"
            # content is missing
        }
        
        # Act
        response = client.post("/messages/", json=message_data)
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity

    def test_get_messages_by_project(self, client: TestClient, db: Session):
        """Test getting messages filtered by project"""
        # Arrange - Create two projects with messages
        user = User(username="testuser", email="test@example.com")
        project1 = Project(name="Project 1", description="Description 1")
        project2 = Project(name="Project 2", description="Description 2")
        db.add(user)
        db.add(project1)
        db.add(project2)
        db.commit()
        db.refresh(user)
        db.refresh(project1)
        db.refresh(project2)
        
        message1 = Message(
            content="Message for Project 1",
            message_type="comment",
            user_id=user.id,
            project_id=project1.id
        )
        message2 = Message(
            content="Message for Project 2",
            message_type="comment",
            user_id=user.id,
            project_id=project2.id
        )
        db.add(message1)
        db.add(message2)
        db.commit()
        
        # Act
        response = client.get(f"/messages/?project_id={project1.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["project_id"] == project1.id
        assert data[0]["content"] == "Message for Project 1"

    def test_get_messages_by_task(self, client: TestClient, db: Session):
        """Test getting messages filtered by task"""
        # Arrange - Create tasks with messages
        user = User(username="testuser", email="test@example.com")
        project = Project(name="Test Project", description="Test Description")
        db.add(user)
        db.add(project)
        db.commit()
        db.refresh(user)
        db.refresh(project)
        
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
            status="pending",
            project_id=project.id,
            assignee_id=user.id
        )
        db.add(task1)
        db.add(task2)
        db.commit()
        db.refresh(task1)
        db.refresh(task2)
        
        message1 = Message(
            content="Message for Task 1",
            message_type="comment",
            user_id=user.id,
            project_id=project.id,
            task_id=task1.id
        )
        message2 = Message(
            content="Message for Task 2",
            message_type="comment",
            user_id=user.id,
            project_id=project.id,
            task_id=task2.id
        )
        db.add(message1)
        db.add(message2)
        db.commit()
        
        # Act
        response = client.get(f"/messages/?task_id={task1.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["task_id"] == task1.id
        assert data[0]["content"] == "Message for Task 1"

    def test_get_messages_by_user(self, client: TestClient, db: Session):
        """Test getting messages filtered by user"""
        # Arrange - Create two users with messages
        user1 = User(username="user1", email="user1@example.com")
        user2 = User(username="user2", email="user2@example.com")
        project = Project(name="Test Project", description="Test Description")
        db.add(user1)
        db.add(user2)
        db.add(project)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        db.refresh(project)
        
        message1 = Message(
            content="Message from User 1",
            message_type="comment",
            user_id=user1.id,
            project_id=project.id
        )
        message2 = Message(
            content="Message from User 2",
            message_type="comment",
            user_id=user2.id,
            project_id=project.id
        )
        db.add(message1)
        db.add(message2)
        db.commit()
        
        # Act
        response = client.get(f"/messages/?user_id={user1.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["user_id"] == user1.id
        assert data[0]["content"] == "Message from User 1"

    def test_create_reply_message(self, client: TestClient, db: Session):
        """Test creating a reply to another message"""
        # Arrange - Create parent message
        user = User(username="testuser", email="test@example.com")
        project = Project(name="Test Project", description="Test Description")
        db.add(user)
        db.add(project)
        db.commit()
        db.refresh(user)
        db.refresh(project)
        
        parent_message = Message(
            content="Parent message",
            message_type="comment",
            user_id=user.id,
            project_id=project.id
        )
        db.add(parent_message)
        db.commit()
        db.refresh(parent_message)
        
        reply_data = {
            "content": "This is a reply",
            "message_type": "comment",
            "user_id": user.id,
            "project_id": project.id,
            "parent_id": parent_message.id
        }
        
        # Act
        response = client.post("/messages/", json=reply_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["parent_id"] == parent_message.id
        assert data["content"] == reply_data["content"] 