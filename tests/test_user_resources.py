"""
Tests for user-related MCP resources
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.resources.user_resources import user_resource_handler
from app.models.user import User as UserModel


class TestUserResources:
    """Test suite for user MCP resources"""

    def test_user_resource_handler_success(self):
        """Test successful user resource retrieval"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 1
        expected_user = UserModel(
            id=user_id,
            username="testuser",
            email="test@example.com"
        )
        
        with patch('app.resources.user_resources.get_db') as mock_get_db:
            with patch('app.resources.user_resources.crud.user.get_user') as mock_get_user:
                mock_get_db.return_value = iter([mock_db])
                mock_get_user.return_value = expected_user
                
                # Act
                result = user_resource_handler(user_id)
                
                # Assert
                assert "id" in result
                assert result["id"] == user_id
                assert result["username"] == "testuser"
                assert result["email"] == "test@example.com"
                mock_get_user.assert_called_once_with(db=mock_db, user_id=user_id)

    def test_user_resource_handler_not_found(self):
        """Test user resource retrieval when user doesn't exist"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 999
        
        with patch('app.resources.user_resources.get_db') as mock_get_db:
            with patch('app.resources.user_resources.crud.user.get_user') as mock_get_user:
                mock_get_db.return_value = iter([mock_db])
                mock_get_user.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="User not found"):
                    user_resource_handler(user_id)

    def test_user_resource_handler_invalid_id(self):
        """Test user resource retrieval with invalid ID type"""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid user ID"):
            user_resource_handler("invalid")

    def test_user_resource_handler_with_tasks(self):
        """Test user resource retrieval including assigned tasks"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 1
        expected_user = UserModel(
            id=user_id,
            username="testuser",
            email="test@example.com"
        )
        
        with patch('app.resources.user_resources.get_db') as mock_get_db:
            with patch('app.resources.user_resources.crud.user.get_user') as mock_get_user:
                with patch('app.resources.user_resources.crud.task.get_tasks') as mock_get_tasks:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_user.return_value = expected_user
                    mock_get_tasks.return_value = []  # Empty tasks for simplicity
                    
                    # Act
                    result = user_resource_handler(user_id, include_tasks=True)
                    
                    # Assert
                    assert "tasks" in result
                    assert isinstance(result["tasks"], list)
                    mock_get_tasks.assert_called_once_with(db=mock_db, assignee_id=user_id)

    def test_user_resource_handler_with_messages(self):
        """Test user resource retrieval including user messages"""
        # Arrange
        mock_db = Mock(spec=Session)
        user_id = 1
        expected_user = UserModel(
            id=user_id,
            username="testuser",
            email="test@example.com"
        )
        
        with patch('app.resources.user_resources.get_db') as mock_get_db:
            with patch('app.resources.user_resources.crud.user.get_user') as mock_get_user:
                with patch('app.resources.user_resources.crud.message.get_messages') as mock_get_messages:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_user.return_value = expected_user
                    mock_get_messages.return_value = []  # Empty messages for simplicity
                    
                    # Act
                    result = user_resource_handler(user_id, include_messages=True)
                    
                    # Assert
                    assert "messages" in result
                    assert isinstance(result["messages"], list)
                    mock_get_messages.assert_called_once_with(db=mock_db, user_id=user_id, limit=50)

    def test_user_resource_handler_by_username(self):
        """Test user resource retrieval by username"""
        # Arrange
        mock_db = Mock(spec=Session)
        username = "testuser"
        expected_user = UserModel(
            id=1,
            username=username,
            email="test@example.com"
        )
        
        with patch('app.resources.user_resources.get_db') as mock_get_db:
            with patch('app.resources.user_resources.crud.user.get_user_by_username') as mock_get_user_by_username:
                mock_get_db.return_value = iter([mock_db])
                mock_get_user_by_username.return_value = expected_user
                
                # Act
                result = user_resource_handler(username, lookup_by_username=True)
                
                # Assert
                assert result["id"] == 1
                assert result["username"] == username
                assert result["email"] == "test@example.com"
                mock_get_user_by_username.assert_called_once_with(db=mock_db, username=username) 