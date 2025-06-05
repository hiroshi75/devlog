"""
Tests for message-related MCP resources
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.resources.message_resources import messages_recent_resource_handler
from app.models.message import Message as MessageModel


class TestMessageResources:
    """Test suite for message MCP resources"""

    def test_messages_recent_resource_handler_success(self):
        """Test successful recent messages resource retrieval"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_messages = [
            MessageModel(
                id=1,
                content="Message 1",
                message_type="status_update",
                user_id=1,
                project_id=1
            ),
            MessageModel(
                id=2,
                content="Message 2",
                message_type="comment",
                user_id=2,
                task_id=1
            )
        ]
        
        with patch('app.resources.message_resources.get_db') as mock_get_db:
            with patch('app.resources.message_resources.crud.message.get_messages') as mock_get_messages:
                mock_get_db.return_value = iter([mock_db])
                mock_get_messages.return_value = expected_messages
                
                # Act
                result = messages_recent_resource_handler()
                
                # Assert
                assert "messages" in result
                assert len(result["messages"]) == 2
                assert result["messages"][0]["id"] == 1
                assert result["messages"][0]["content"] == "Message 1"
                assert result["messages"][1]["id"] == 2
                assert result["messages"][1]["content"] == "Message 2"
                mock_get_messages.assert_called_once_with(
                    db=mock_db, 
                    project_id=None, 
                    task_id=None, 
                    user_id=None, 
                    message_type=None, 
                    limit=50
                )

    def test_messages_recent_resource_handler_with_limit(self):
        """Test recent messages resource retrieval with custom limit"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_messages = [
            MessageModel(id=1, content="Message 1", message_type="status_update", user_id=1)
        ]
        
        with patch('app.resources.message_resources.get_db') as mock_get_db:
            with patch('app.resources.message_resources.crud.message.get_messages') as mock_get_messages:
                mock_get_db.return_value = iter([mock_db])
                mock_get_messages.return_value = expected_messages
                
                # Act
                result = messages_recent_resource_handler(limit=10)
                
                # Assert
                assert "messages" in result
                assert len(result["messages"]) == 1
                mock_get_messages.assert_called_once_with(
                    db=mock_db, 
                    project_id=None, 
                    task_id=None, 
                    user_id=None, 
                    message_type=None, 
                    limit=10
                )

    def test_messages_recent_resource_handler_with_project_filter(self):
        """Test recent messages resource retrieval filtered by project"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 1
        expected_messages = [
            MessageModel(
                id=1,
                content="Project Message",
                message_type="status_update",
                user_id=1,
                project_id=project_id
            )
        ]
        
        with patch('app.resources.message_resources.get_db') as mock_get_db:
            with patch('app.resources.message_resources.crud.message.get_messages') as mock_get_messages:
                mock_get_db.return_value = iter([mock_db])
                mock_get_messages.return_value = expected_messages
                
                # Act
                result = messages_recent_resource_handler(project_id=project_id)
                
                # Assert
                assert "messages" in result
                assert len(result["messages"]) == 1
                assert result["messages"][0]["project_id"] == project_id
                mock_get_messages.assert_called_once_with(
                    db=mock_db, 
                    project_id=project_id, 
                    task_id=None, 
                    user_id=None, 
                    message_type=None, 
                    limit=50
                )

    def test_messages_recent_resource_handler_with_task_filter(self):
        """Test recent messages resource retrieval filtered by task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        expected_messages = [
            MessageModel(
                id=1,
                content="Task Message",
                message_type="comment",
                user_id=1,
                task_id=task_id
            )
        ]
        
        with patch('app.resources.message_resources.get_db') as mock_get_db:
            with patch('app.resources.message_resources.crud.message.get_messages') as mock_get_messages:
                mock_get_db.return_value = iter([mock_db])
                mock_get_messages.return_value = expected_messages
                
                # Act
                result = messages_recent_resource_handler(task_id=task_id)
                
                # Assert
                assert "messages" in result
                assert len(result["messages"]) == 1
                assert result["messages"][0]["task_id"] == task_id
                mock_get_messages.assert_called_once_with(
                    db=mock_db, 
                    project_id=None, 
                    task_id=task_id, 
                    user_id=None, 
                    message_type=None, 
                    limit=50
                )

    def test_messages_recent_resource_handler_with_user_info(self):
        """Test recent messages resource retrieval including user information"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_messages = [
            MessageModel(
                id=1,
                content="Message with user info",
                message_type="status_update",
                user_id=1
            )
        ]
        
        mock_user = Mock()
        mock_user.id = 1
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        
        with patch('app.resources.message_resources.get_db') as mock_get_db:
            with patch('app.resources.message_resources.crud.message.get_messages') as mock_get_messages:
                with patch('app.resources.message_resources.crud.user.get_user') as mock_get_user:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_messages.return_value = expected_messages
                    mock_get_user.return_value = mock_user
                    
                    # Act
                    result = messages_recent_resource_handler(include_user_info=True)
                    
                    # Assert
                    assert "messages" in result
                    assert len(result["messages"]) == 1
                    message = result["messages"][0]
                    assert "user" in message
                    assert message["user"]["username"] == "testuser"
                    mock_get_user.assert_called_once_with(db=mock_db, user_id=1)

    def test_messages_recent_resource_handler_empty_result(self):
        """Test recent messages resource retrieval with no messages"""
        # Arrange
        mock_db = Mock(spec=Session)
        
        with patch('app.resources.message_resources.get_db') as mock_get_db:
            with patch('app.resources.message_resources.crud.message.get_messages') as mock_get_messages:
                mock_get_db.return_value = iter([mock_db])
                mock_get_messages.return_value = []
                
                # Act
                result = messages_recent_resource_handler()
                
                # Assert
                assert "messages" in result
                assert len(result["messages"]) == 0
                assert result["total_count"] == 0 