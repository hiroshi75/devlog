"""
Tests for project-related MCP tools
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.tools.project_tools import (
    create_project_tool,
    get_projects_tool,
    get_project_tool,
    update_project_tool,
    delete_project_tool,
)
from app.models.project import Project as ProjectModel


class TestProjectTools:
    """Test suite for project MCP tools"""

    def test_create_project_tool_success(self):
        """Test successful project creation"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_data = {
            "name": "Test Project",
            "description": "Test Description"
        }
        expected_project = ProjectModel(
            id=1,
            name="Test Project",
            description="Test Description"
        )
        
        with patch('app.tools.project_tools.get_db') as mock_get_db:
            with patch('app.tools.project_tools.crud.project.create_project') as mock_create:
                mock_get_db.return_value = iter([mock_db])
                mock_create.return_value = expected_project
                
                # Act
                result = create_project_tool(
                    name=project_data["name"],
                    description=project_data["description"]
                )
                
                # Assert
                assert result["id"] == 1
                assert result["name"] == "Test Project"
                assert result["description"] == "Test Description"
                mock_create.assert_called_once()

    def test_create_project_tool_missing_name(self):
        """Test project creation with missing name"""
        # Act & Assert
        with pytest.raises(ValueError, match="Project name is required"):
            create_project_tool(name="", description="Test")

    def test_get_projects_tool_success(self):
        """Test getting all projects"""
        # Arrange
        mock_db = Mock(spec=Session)
        expected_projects = [
            ProjectModel(id=1, name="Project 1", description="Desc 1"),
            ProjectModel(id=2, name="Project 2", description="Desc 2")
        ]
        
        with patch('app.tools.project_tools.get_db') as mock_get_db:
            with patch('app.tools.project_tools.crud.project.get_projects') as mock_get_projects:
                mock_get_db.return_value = iter([mock_db])
                mock_get_projects.return_value = expected_projects
                
                # Act
                result = get_projects_tool()
                
                # Assert
                assert len(result) == 2
                assert result[0]["id"] == 1
                assert result[0]["name"] == "Project 1"
                assert result[1]["id"] == 2
                assert result[1]["name"] == "Project 2"

    def test_get_project_tool_success(self):
        """Test getting a specific project"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 1
        expected_project = ProjectModel(
            id=project_id,
            name="Test Project",
            description="Test Description"
        )
        
        with patch('app.tools.project_tools.get_db') as mock_get_db:
            with patch('app.tools.project_tools.crud.project.get_project') as mock_get_project:
                mock_get_db.return_value = iter([mock_db])
                mock_get_project.return_value = expected_project
                
                # Act
                result = get_project_tool(project_id=project_id)
                
                # Assert
                assert result["id"] == project_id
                assert result["name"] == "Test Project"
                assert result["description"] == "Test Description"

    def test_get_project_tool_not_found(self):
        """Test getting a non-existent project"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 999
        
        with patch('app.tools.project_tools.get_db') as mock_get_db:
            with patch('app.tools.project_tools.crud.project.get_project') as mock_get_project:
                mock_get_db.return_value = iter([mock_db])
                mock_get_project.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Project not found"):
                    get_project_tool(project_id=project_id)

    def test_update_project_tool_success(self):
        """Test updating a project"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 1
        update_data = {
            "name": "Updated Project",
            "description": "Updated Description"
        }
        existing_project = ProjectModel(
            id=project_id,
            name="Old Project",
            description="Old Description"
        )
        updated_project = ProjectModel(
            id=project_id,
            name="Updated Project",
            description="Updated Description"
        )
        
        with patch('app.tools.project_tools.get_db') as mock_get_db:
            with patch('app.tools.project_tools.crud.project.get_project') as mock_get_project:
                with patch('app.tools.project_tools.crud.project.update_project') as mock_update:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_project.return_value = existing_project
                    mock_update.return_value = updated_project
                    
                    # Act
                    result = update_project_tool(
                        project_id=project_id,
                        name=update_data["name"],
                        description=update_data["description"]
                    )
                    
                    # Assert
                    assert result["id"] == project_id
                    assert result["name"] == "Updated Project"
                    assert result["description"] == "Updated Description"

    def test_update_project_tool_not_found(self):
        """Test updating a non-existent project"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 999
        
        with patch('app.tools.project_tools.get_db') as mock_get_db:
            with patch('app.tools.project_tools.crud.project.get_project') as mock_get_project:
                mock_get_db.return_value = iter([mock_db])
                mock_get_project.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Project not found"):
                    update_project_tool(
                        project_id=project_id,
                        name="Updated"
                    )

    def test_delete_project_tool_success(self):
        """Test deleting a project"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 1
        existing_project = ProjectModel(
            id=project_id,
            name="Test Project",
            description="Test Description"
        )
        
        with patch('app.tools.project_tools.get_db') as mock_get_db:
            with patch('app.tools.project_tools.crud.project.get_project') as mock_get_project:
                with patch('app.tools.project_tools.crud.project.delete_project') as mock_delete:
                    mock_get_db.return_value = iter([mock_db])
                    mock_get_project.return_value = existing_project
                    mock_delete.return_value = True
                    
                    # Act
                    result = delete_project_tool(project_id=project_id)
                    
                    # Assert
                    assert result["success"] is True
                    assert result["message"] == f"Project {project_id} deleted successfully"

    def test_delete_project_tool_not_found(self):
        """Test deleting a non-existent project"""
        # Arrange
        mock_db = Mock(spec=Session)
        project_id = 999
        
        with patch('app.tools.project_tools.get_db') as mock_get_db:
            with patch('app.tools.project_tools.crud.project.get_project') as mock_get_project:
                mock_get_db.return_value = iter([mock_db])
                mock_get_project.return_value = None
                
                # Act & Assert
                with pytest.raises(ValueError, match="Project not found"):
                    delete_project_tool(project_id=project_id) 