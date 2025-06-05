"""
Tests for message-related MCP tools
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.tools.message_tools import (
    create_message_tool,
    get_messages_tool,
    get_message_tool,
)
from app.models.message import Message as MessageModel


class TestMessageTools:
    """Test suite for message MCP tools"""

    def test_create_message_tool_success(self):
        """Test successful message creation"""
        # Arrange
        mock_db = Mock(spec=Session)
        message_data = {
            "content": "Test message content",
            "message_type": "status_update",
            "user_id": 1,
            "project_id": 1
        }
        expected_message = MessageModel(
            id=1,
            content="Test message content",
            message_type="status_update",
            user_id=1,
            project_id=1
        )
        
        with patch('app.tools.message_tools.get_db') as mock_get_db:
            with patch('app.tools.message_tools.crud.message.create_message') as mock_create:
                mock_get_db.return_value = iter([mock_db])
                mock_create.return_value = expected_message
                
                # Act
                result = create_message_tool(
                    content=message_data["content"],
                    message_type=message_data["message_type"],
                    user_id=message_data["user_id"],
                    project_id=message_data["project_id"]
                )
                
                # Assert
                assert result["id"] == 1
                assert result["content"] == "Test message content"
                assert result["message_type"] == "status_update"
                assert result["user_id"] == 1
                assert result["project_id"] == 1
                mock_create.assert_called_once()

    def test_create_message_tool_missing_content(self):
        """Test message creation with missing content"""
        # Act & Assert
        with pytest.raises(ValueError, match="Message content is required"):
            create_message_tool(content="", message_type="status_update", user_id=1)

    def test_create_message_tool_missing_user_id(self):
        """Test message creation with missing user_id"""
        # Act & Assert
        with pytest.raises(ValueError, match="User ID is required"):
            create_message_tool(content="Test", message_type="status_update")

    def test_create_message_tool_with_task_id(self):
        """Test message creation with task_id"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_message = MessageModel(
            id=1,
            content="Task message",
            message_type="comment",
            user_id=1,
            task_id=1
        )
        
        with patch('app.tools.message_tools.get_db') as mock_get_db:
            with patch('app.tools.message_tools.crud.message.create_message') as mock_create:
                mock_get_db.return_value = iter([mock_db])
                mock_create.return_value = expected_message
                
                # Act
                result = create_message_tool(
                    content="Task message",
                    message_type="comment",
                    user_id=1,
                    task_id=1
                )
                
                # Assert
                assert result["task_id"] == 1
                assert result["content"] == "Task message"

    def test_get_messages_tool_success(self):
        """Test getting all messages"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_messages = [
            MessageModel(id=1, content="Message 1", message_type="status_update", user_id=1),
            MessageModel(id=2, content="Message 2", message_type="comment", user_id=2)
        ]
        
        with patch('app.tools.message_tools.get_db') as mock_get_db:
            with patch('app.tools.message_tools.crud.message.get_messages') as mock_get_messages:
                mock_get_db.return_value = iter([mock_db])
                mock_get_messages.return_value = expected_messages
                
                # Act
                result = get_messages_tool()
                
                # Assert
                assert len(result) == 2
                assert result[0]["id"] == 1
                assert result[0]["content"] == "Message 1"
                assert result[1]["id"] == 2
                assert result[1]["content"] == "Message 2"

    def test_get_messages_tool_with_filters(self):
        """Test getting messages with filters"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_messages = [
            MessageModel(id=1, content="Message 1", message_type="status_update", user_id=1, project_id=1)
        ]
        
        with patch('app.tools.message_tools.get_db') as mock_get_db:
            with patch('app.tools.message_tools.crud.message.get_messages') as mock_get_messages:
                mock_get_db.return_value = iter([mock_db])
                mock_get_messages.return_value = expected_messages
                
                # Act
                result = get_messages_tool(project_id=1, message_type="status_update")
                
                # Assert
                assert len(result) == 1
                assert result[0]["project_id"] == 1
                assert result[0]["message_type"] == "status_update"

    def test_get_message_tool_success(self):
        """Test getting a specific message"""
        # Arrange
        mock_db = Mock(spec=Session)
        message_id = 1
        expected_message = MessageModel(
            id=message_id,
            content="Test message",
            message_type="status_update",
            user_id=1,
            project_id=1
        )
        
        with patch('app.tools.message_tools.get_db') as mock_get_db:
            with patch('app.tools.message_tools.crud.message.get_message') as mock_get_message:
                mock_get_db.return_value = iter([mock_db])
                mock_get_message.return_value = expected_message
                
                # Act
                result = get_message_tool(message_id=message_id)
                
                # Assert
                assert result["id"] == message_id
                assert result["content"] == "Test message"
                assert result["message_type"] == "status_update"
                assert result["user_id"] == 1

    def test_get_message_tool_not_found(self):
        """Test getting a non-existent message"""
        # Arrange
        mock_db = Mock(spec=Session)
        message_id = 999
        
        with patch('app.tools.message_tools.get_db') as mock_get_db:
            with patch('app.tools.message_tools.crud.message.get_message') as mock_get_message:
                mock_get_db.return_value = iter([mock_db])
                mock_get_message.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Message not found"):
                    get_message_tool(message_id=message_id) 