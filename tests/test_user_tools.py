"""
Tests for user-related MCP tools
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.tools.user_tools import (
    create_user_tool,
    get_users_tool,
    get_user_tool,
)
from app.models.user import User as UserModel


class TestUserTools:
    """Test suite for user MCP tools"""

    def test_create_user_tool_success(self):
        """Test successful user creation"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        expected_user = UserModel(
            id=1,
            username="testuser",
            email="test@example.com"
        )
        
        with patch('app.tools.user_tools.get_db') as mock_get_db:
            with patch('app.tools.user_tools.crud.user.create_user') as mock_create:
                mock_get_db.return_value = iter([mock_db])
                mock_create.return_value = expected_user
                
                # Act
                result = create_user_tool(
                    username=user_data["username"],
                    email=user_data["email"]
                )
                
                # Assert
                assert result["id"] == 1
                assert result["username"] == "testuser"
                assert result["email"] == "test@example.com"
                mock_create.assert_called_once()

    def test_create_user_tool_missing_username(self):
        """Test user creation with missing username"""
        # Act & Assert
        with pytest.raises(ValueError, match="Username is required"):
            create_user_tool(username="", email="test@example.com")

    def test_create_user_tool_missing_email(self):
        """Test user creation with missing email"""
        # Act & Assert
        with pytest.raises(ValueError, match="Email is required"):
            create_user_tool(username="testuser", email="")

    def test_create_user_tool_invalid_email(self):
        """Test user creation with invalid email format"""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email format"):
            create_user_tool(username="testuser", email="invalid-email")

    def test_get_users_tool_success(self):
        """Test getting all users"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_users = [
            UserModel(id=1, username="user1", email="user1@example.com"),
            UserModel(id=2, username="user2", email="user2@example.com")
        ]
        
        with patch('app.tools.user_tools.get_db') as mock_get_db:
            with patch('app.tools.user_tools.crud.user.get_users') as mock_get_users:
                mock_get_db.return_value = iter([mock_db])
                mock_get_users.return_value = expected_users
                
                # Act
                result = get_users_tool()
                
                # Assert
                assert len(result) == 2
                assert result[0]["id"] == 1
                assert result[0]["username"] == "user1"
                assert result[1]["id"] == 2
                assert result[1]["username"] == "user2"

    def test_get_user_tool_success(self):
        """Test getting a specific user"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 1
        expected_user = UserModel(
            id=user_id,
            username="testuser",
            email="test@example.com"
        )
        
        with patch('app.tools.user_tools.get_db') as mock_get_db:
            with patch('app.tools.user_tools.crud.user.get_user') as mock_get_user:
                mock_get_db.return_value = iter([mock_db])
                mock_get_user.return_value = expected_user
                
                # Act
                result = get_user_tool(user_id=user_id)
                
                # Assert
                assert result["id"] == user_id
                assert result["username"] == "testuser"
                assert result["email"] == "test@example.com"

    def test_get_user_tool_not_found(self):
        """Test getting a non-existent user"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 999
        
        with patch('app.tools.user_tools.get_db') as mock_get_db:
            with patch('app.tools.user_tools.crud.user.get_user') as mock_get_user:
                mock_get_db.return_value = iter([mock_db])
                mock_get_user.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="User not found"):
                    get_user_tool(user_id=user_id)

    def test_get_user_tool_by_username_success(self):
        """Test getting a user by username"""
        # Arrange
        mock_db = Mock(spec=Session)
        username = "testuser"
        expected_user = UserModel(
            id=1,
            username="testuser",
            email="test@example.com"
        )
        
        with patch('app.tools.user_tools.get_db') as mock_get_db:
            with patch('app.tools.user_tools.crud.user.get_user_by_username') as mock_get_user:
                mock_get_db.return_value = iter([mock_db])
                mock_get_user.return_value = expected_user
                
                # Act
                result = get_user_tool(username=username)
                
                # Assert
                assert result["id"] == 1
                assert result["username"] == "testuser"
                assert result["email"] == "test@example.com"

    def test_get_user_tool_missing_parameters(self):
        """Test getting a user without both user_id and username"""
        # Act & Assert
        with pytest.raises(ValueError, match="Either user_id or username must be provided"):
            get_user_tool() 