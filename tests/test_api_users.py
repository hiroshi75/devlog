"""
Tests for user API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate


class TestUserAPI:
    """Test cases for user API endpoints"""

    def test_create_user(self, client: TestClient, db: Session):
        """Test creating a new user"""
        # Arrange
        user_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        
        # Act
        response = client.post("/users/", json=user_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_get_users(self, client: TestClient, db: Session):
        """Test getting all users"""
        # Arrange - Create test users
        user1 = User(username="user1", email="user1@example.com")
        user2 = User(username="user2", email="user2@example.com")
        db.add(user1)
        db.add(user2)
        db.commit()
        
        # Act
        response = client.get("/users/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        usernames = [u["username"] for u in data]
        assert "user1" in usernames
        assert "user2" in usernames

    def test_get_user_by_id(self, client: TestClient, db: Session):
        """Test getting a specific user by ID"""
        # Arrange
        user = User(username="testuser", email="test@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Act
        response = client.get(f"/users/{user.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user.id
        assert data["username"] == user.username
        assert data["email"] == user.email

    def test_get_user_not_found(self, client: TestClient):
        """Test getting a non-existent user"""
        # Act
        response = client.get("/users/999999")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_create_user_invalid_data(self, client: TestClient):
        """Test creating a user with invalid data"""
        # Arrange - Missing required field
        user_data = {
            "username": "testuser"
            # email is missing
        }
        
        # Act
        response = client.post("/users/", json=user_data)
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity

    def test_create_user_duplicate_username(self, client: TestClient, db: Session):
        """Test creating a user with duplicate username"""
        # Arrange - Create existing user
        existing_user = User(username="testuser", email="existing@example.com")
        db.add(existing_user)
        db.commit()
        
        # Try to create user with same username
        user_data = {
            "username": "testuser",
            "email": "new@example.com"
        }
        
        # Act
        response = client.post("/users/", json=user_data)
        
        # Assert
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_create_user_duplicate_email(self, client: TestClient, db: Session):
        """Test creating a user with duplicate email"""
        # Arrange - Create existing user
        existing_user = User(username="existinguser", email="test@example.com")
        db.add(existing_user)
        db.commit()
        
        # Try to create user with same email
        user_data = {
            "username": "newuser",
            "email": "test@example.com"
        }
        
        # Act
        response = client.post("/users/", json=user_data)
        
        # Assert
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_get_user_by_username(self, client: TestClient, db: Session):
        """Test getting a user by username query parameter"""
        # Arrange
        user = User(username="testuser", email="test@example.com")
        db.add(user)
        db.commit()
        
        # Act
        response = client.get("/users/?username=testuser")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["username"] == "testuser"

    def test_get_user_by_email(self, client: TestClient, db: Session):
        """Test getting a user by email query parameter"""
        # Arrange
        user = User(username="testuser", email="test@example.com")
        db.add(user)
        db.commit()
        
        # Act
        response = client.get("/users/?email=test@example.com")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["email"] == "test@example.com" 