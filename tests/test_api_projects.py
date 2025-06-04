"""
Tests for project API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.project import Project
from app.schemas.project import ProjectCreate


class TestProjectAPI:
    """Test cases for project API endpoints"""

    def test_create_project(self, client: TestClient, db: Session):
        """Test creating a new project"""
        # Arrange
        project_data = {
            "name": "Test Project",
            "description": "This is a test project"
        }
        
        # Act
        response = client.post("/projects/", json=project_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == project_data["name"]
        assert data["description"] == project_data["description"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_projects(self, client: TestClient, db: Session):
        """Test getting all projects"""
        # Arrange - Create test projects
        project1 = Project(name="Project 1", description="Description 1")
        project2 = Project(name="Project 2", description="Description 2")
        db.add(project1)
        db.add(project2)
        db.commit()
        
        # Act
        response = client.get("/projects/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        project_names = [p["name"] for p in data]
        assert "Project 1" in project_names
        assert "Project 2" in project_names

    def test_get_project_by_id(self, client: TestClient, db: Session):
        """Test getting a specific project by ID"""
        # Arrange
        project = Project(name="Test Project", description="Test Description")
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # Act
        response = client.get(f"/projects/{project.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project.id
        assert data["name"] == project.name
        assert data["description"] == project.description

    def test_get_project_not_found(self, client: TestClient):
        """Test getting a non-existent project"""
        # Act
        response = client.get("/projects/999999")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Project not found"

    def test_update_project(self, client: TestClient, db: Session):
        """Test updating a project"""
        # Arrange
        project = Project(name="Original Name", description="Original Description")
        db.add(project)
        db.commit()
        db.refresh(project)
        
        update_data = {
            "name": "Updated Name",
            "description": "Updated Description"
        }
        
        # Act
        response = client.put(f"/projects/{project.id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project.id
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]

    def test_update_project_not_found(self, client: TestClient):
        """Test updating a non-existent project"""
        # Arrange
        update_data = {
            "name": "Updated Name",
            "description": "Updated Description"
        }
        
        # Act
        response = client.put("/projects/999999", json=update_data)
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Project not found"

    def test_delete_project(self, client: TestClient, db: Session):
        """Test deleting a project"""
        # Arrange
        project = Project(name="To Delete", description="Will be deleted")
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # Act
        response = client.delete(f"/projects/{project.id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verify project is deleted
        deleted_project = db.query(Project).filter(Project.id == project.id).first()
        assert deleted_project is None

    def test_delete_project_not_found(self, client: TestClient):
        """Test deleting a non-existent project"""
        # Act
        response = client.delete("/projects/999999")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Project not found"

    def test_create_project_invalid_data(self, client: TestClient):
        """Test creating a project with invalid data"""
        # Arrange - Missing required field
        project_data = {
            "description": "Missing name field"
        }
        
        # Act
        response = client.post("/projects/", json=project_data)
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity

    def test_update_project_partial(self, client: TestClient, db: Session):
        """Test partial update of a project"""
        # Arrange
        project = Project(name="Original Name", description="Original Description")
        db.add(project)
        db.commit()
        db.refresh(project)
        
        update_data = {
            "name": "Updated Name Only"
            # description is not provided
        }
        
        # Act
        response = client.put(f"/projects/{project.id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == project.description  # Should remain unchanged 