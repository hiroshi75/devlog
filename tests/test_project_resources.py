"""
Tests for project-related MCP resources
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.resources.project_resources import project_resource_handler
from app.models.project import Project as ProjectModel


class TestProjectResources:
    """Test suite for project MCP resources"""

    def test_project_resource_handler_success(self):
        """Test successful project resource retrieval"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 1
        expected_project = ProjectModel(
            id=project_id,
            name="Test Project",
            description="Test Description"
        )
        
        with patch('app.resources.project_resources.get_db') as mock_get_db:
            with patch('app.resources.project_resources.crud.project.get_project') as mock_get_project:
                mock_get_db.return_value = iter([mock_db])
                mock_get_project.return_value = expected_project
                
                # Act
                result = project_resource_handler(project_id)
                
                # Assert
                assert "id" in result
                assert result["id"] == project_id
                assert result["name"] == "Test Project"
                assert result["description"] == "Test Description"
                mock_get_project.assert_called_once_with(db=mock_db, project_id=project_id)

    def test_project_resource_handler_not_found(self):
        """Test project resource retrieval when project doesn't exist"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 999
        
        with patch('app.resources.project_resources.get_db') as mock_get_db:
            with patch('app.resources.project_resources.crud.project.get_project') as mock_get_project:
                mock_get_db.return_value = iter([mock_db])
                mock_get_project.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Project not found"):
                    project_resource_handler(project_id)

    def test_project_resource_handler_invalid_id(self):
        """Test project resource retrieval with invalid ID type"""
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid project ID"):
            project_resource_handler("invalid")

    def test_project_resource_handler_with_tasks(self):
        """Test project resource retrieval including related tasks"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 1
        expected_project = ProjectModel(
            id=project_id,
            name="Test Project",
            description="Test Description"
        )
        
        with patch('app.resources.project_resources.get_db') as mock_get_db:
            with patch('app.resources.project_resources.crud.project.get_project') as mock_get_project:
                with patch('app.resources.project_resources.crud.task.get_tasks') as mock_get_tasks:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_project.return_value = expected_project
                    mock_get_tasks.return_value = []  # Empty tasks for simplicity
                    
                    # Act
                    result = project_resource_handler(project_id, include_tasks=True)
                    
                    # Assert
                    assert "tasks" in result
                    assert isinstance(result["tasks"], list)
                    mock_get_tasks.assert_called_once_with(db=mock_db, project_id=project_id) 