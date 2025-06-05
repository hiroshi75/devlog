"""
Tests for task-related MCP resources
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.resources.task_resources import task_resource_handler
from app.models.task import Task as TaskModel


class TestTaskResources:
    """Test suite for task MCP resources"""

    def test_task_resource_handler_success(self):
        """Test successful task resource retrieval"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        expected_task = TaskModel(
            id=task_id,
            title="Test Task",
            description="Test Description",
            status="pending",
            project_id=1,
            assignee_id=2
        )
        
        with patch('app.resources.task_resources.get_db') as mock_get_db:
            with patch('app.resources.task_resources.crud.task.get_task') as mock_get_task:
                mock_get_db.return_value = iter([mock_db])
                mock_get_task.return_value = expected_task
                
                # Act
                result = task_resource_handler(task_id)
                
                # Assert
                assert "id" in result
                assert result["id"] == task_id
                assert result["title"] == "Test Task"
                assert result["description"] == "Test Description"
                assert result["status"] == "pending"
                assert result["project_id"] == 1
                assert result["assignee_id"] == 2
                mock_get_task.assert_called_once_with(db=mock_db, task_id=task_id)

    def test_task_resource_handler_not_found(self):
        """Test task resource retrieval when task doesn't exist"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 999
        
        with patch('app.resources.task_resources.get_db') as mock_get_db:
            with patch('app.resources.task_resources.crud.task.get_task') as mock_get_task:
                mock_get_db.return_value = iter([mock_db])
                mock_get_task.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Task not found"):
                    task_resource_handler(task_id)

    def test_task_resource_handler_invalid_id(self):
        """Test task resource retrieval with invalid ID type"""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid task ID"):
            task_resource_handler("invalid")

    def test_task_resource_handler_with_messages(self):
        """Test task resource retrieval including related messages"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        expected_task = TaskModel(
            id=task_id,
            title="Test Task",
            description="Test Description",
            status="pending",
            project_id=1
        )
        
        with patch('app.resources.task_resources.get_db') as mock_get_db:
            with patch('app.resources.task_resources.crud.task.get_task') as mock_get_task:
                with patch('app.resources.task_resources.crud.message.get_messages') as mock_get_messages:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_task.return_value = expected_task
                    mock_get_messages.return_value = []  # Empty messages for simplicity
                    
                    # Act
                    result = task_resource_handler(task_id, include_messages=True)
                    
                    # Assert
                    assert "messages" in result
                    assert isinstance(result["messages"], list)
                    mock_get_messages.assert_called_once_with(db=mock_db, task_id=task_id)

    def test_task_resource_handler_with_project_info(self):
        """Test task resource retrieval including project information"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        expected_task = TaskModel(
            id=task_id,
            title="Test Task",
            description="Test Description",
            status="pending",
            project_id=1
        )
        
        mock_project = Mock()
        mock_project.id = 1
        mock_project.name = "Test Project"
        mock_project.description = "Test Project Description"
        
        with patch('app.resources.task_resources.get_db') as mock_get_db:
            with patch('app.resources.task_resources.crud.task.get_task') as mock_get_task:
                with patch('app.resources.task_resources.crud.project.get_project') as mock_get_project:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_task.return_value = expected_task
                    mock_get_project.return_value = mock_project
                    
                    # Act
                    result = task_resource_handler(task_id, include_project=True)
                    
                    # Assert
                    assert "project" in result
                    assert result["project"]["id"] == 1
                    assert result["project"]["name"] == "Test Project"
                    mock_get_project.assert_called_once_with(db=mock_db, project_id=1) 