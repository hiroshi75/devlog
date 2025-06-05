"""
Tests for task-related MCP tools
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.tools.task_tools import (
    create_task_tool,
    get_tasks_tool,
    get_task_tool,
    update_task_tool,
    delete_task_tool,
)
from app.models.task import Task as TaskModel


class TestTaskTools:
    """Test suite for task MCP tools"""

    def test_create_task_tool_success(self):
        """Test successful task creation"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "project_id": 1
        }
        expected_task = TaskModel(
            id=1,
            title="Test Task",
            description="Test Description",
            project_id=1,
            status="pending"
        )
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.create_task') as mock_create:
                mock_get_db.return_value = iter([mock_db])
                mock_create.return_value = expected_task
                
                # Act
                result = create_task_tool(
                    title=task_data["title"],
                    description=task_data["description"],
                    project_id=task_data["project_id"]
                )
                
                # Assert
                assert result["id"] == 1
                assert result["title"] == "Test Task"
                assert result["description"] == "Test Description"
                assert result["project_id"] == 1
                assert result["status"] == "pending"
                mock_create.assert_called_once()

    def test_create_task_tool_missing_title(self):
        """Test task creation with missing title"""
        # Act & Assert
        with pytest.raises(ValueError, match="Task title is required"):
            create_task_tool(title="", description="Test", project_id=1)

    def test_create_task_tool_missing_project_id(self):
        """Test task creation with missing project_id"""
        # Act & Assert
        with pytest.raises(ValueError, match="Project ID is required"):
            create_task_tool(title="Test Task", description="Test")

    def test_get_tasks_tool_success(self):
        """Test getting all tasks"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_tasks = [
            TaskModel(id=1, title="Task 1", description="Desc 1", project_id=1, status="pending"),
            TaskModel(id=2, title="Task 2", description="Desc 2", project_id=1, status="in_progress")
        ]
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.get_tasks') as mock_get_tasks:
                mock_get_db.return_value = iter([mock_db])
                mock_get_tasks.return_value = expected_tasks
                
                # Act
                result = get_tasks_tool()
                
                # Assert
                assert len(result) == 2
                assert result[0]["id"] == 1
                assert result[0]["title"] == "Task 1"
                assert result[1]["id"] == 2
                assert result[1]["title"] == "Task 2"

    def test_get_tasks_tool_with_filters(self):
        """Test getting tasks with filters"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_tasks = [
            TaskModel(id=1, title="Task 1", description="Desc 1", project_id=1, status="pending")
        ]
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.get_tasks') as mock_get_tasks:
                mock_get_db.return_value = iter([mock_db])
                mock_get_tasks.return_value = expected_tasks
                
                # Act
                result = get_tasks_tool(project_id=1, status="pending")
                
                # Assert
                assert len(result) == 1
                assert result[0]["id"] == 1
                assert result[0]["status"] == "pending"

    def test_get_task_tool_success(self):
        """Test getting a specific task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        expected_task = TaskModel(
            id=task_id,
            title="Test Task",
            description="Test Description",
            project_id=1,
            status="pending"
        )
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.get_task') as mock_get_task:
                mock_get_db.return_value = iter([mock_db])
                mock_get_task.return_value = expected_task
                
                # Act
                result = get_task_tool(task_id=task_id)
                
                # Assert
                assert result["id"] == task_id
                assert result["title"] == "Test Task"
                assert result["description"] == "Test Description"
                assert result["project_id"] == 1

    def test_get_task_tool_not_found(self):
        """Test getting a non-existent task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 999
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.get_task') as mock_get_task:
                mock_get_db.return_value = iter([mock_db])
                mock_get_task.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Task not found"):
                    get_task_tool(task_id=task_id)

    def test_update_task_tool_success(self):
        """Test updating a task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        update_data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "in_progress"
        }
        existing_task = TaskModel(
            id=task_id,
            title="Old Task",
            description="Old Description",
            project_id=1,
            status="pending"
        )
        updated_task = TaskModel(
            id=task_id,
            title="Updated Task",
            description="Updated Description",
            project_id=1,
            status="in_progress"
        )
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.get_task') as mock_get_task:
                with patch('app.tools.task_tools.crud.task.update_task') as mock_update:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_task.return_value = existing_task
                    mock_update.return_value = updated_task
                    
                    # Act
                    result = update_task_tool(
                        task_id=task_id,
                        title=update_data["title"],
                        description=update_data["description"],
                        status=update_data["status"]
                    )
                    
                    # Assert
                    assert result["id"] == task_id
                    assert result["title"] == "Updated Task"
                    assert result["description"] == "Updated Description"
                    assert result["status"] == "in_progress"

    def test_update_task_tool_not_found(self):
        """Test updating a non-existent task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 999
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.get_task') as mock_get_task:
                mock_get_db.return_value = iter([mock_db])
                mock_get_task.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Task not found"):
                    update_task_tool(
                        task_id=task_id,
                        title="Updated"
                    )

    def test_delete_task_tool_success(self):
        """Test deleting a task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 1
        existing_task = TaskModel(
            id=task_id,
            title="Test Task",
            description="Test Description",
            project_id=1,
            status="pending"
        )
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.get_task') as mock_get_task:
                with patch('app.tools.task_tools.crud.task.delete_task') as mock_delete:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_task.return_value = existing_task
                    mock_delete.return_value = True
                    
                    # Act
                    result = delete_task_tool(task_id=task_id)
                    
                    # Assert
                    assert result["success"] is True
                    assert result["message"] == f"Task {task_id} deleted successfully"

    def test_delete_task_tool_not_found(self):
        """Test deleting a non-existent task"""
        # Arrange
        mock_db = Mock(spec=Session)
        task_id = 999
        
        with patch('app.tools.task_tools.get_db') as mock_get_db:
            with patch('app.tools.task_tools.crud.task.get_task') as mock_get_task:
                mock_get_db.return_value = iter([mock_db])
                mock_get_task.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Task not found"):
                    delete_task_tool(task_id=task_id) 