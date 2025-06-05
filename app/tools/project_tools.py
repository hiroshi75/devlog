"""
Project-related MCP tools for DevStatusMCP
"""

from typing import Optional, List, Dict, Any

from app.db.database import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.project import Project as ProjectModel
from app import crud


def create_project_tool(name: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new project
    
    Args:
        name: Project name
        description: Project description (optional)
        
    Returns:
        Created project information
        
    Raises:
        ValueError: If project name is empty
    """
    if not name or not name.strip():
        raise ValueError("Project name is required")
    
    db = next(get_db())
    try:
        project_data = ProjectCreate(name=name, description=description)
        project = crud.project.create_project(db=db, project=project_data)
        
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
    finally:
        db.close()


def get_projects_tool() -> List[Dict[str, Any]]:
    """
    Get all projects
    
    Returns:
        List of all projects
    """
    db = next(get_db())
    try:
        projects = crud.project.get_projects(db=db)
        
        return [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at.isoformat() if project.created_at else None,
                "updated_at": project.updated_at.isoformat() if project.updated_at else None
            }
            for project in projects
        ]
    finally:
        db.close()


def get_project_tool(project_id: int) -> Dict[str, Any]:
    """
    Get a specific project by ID
    
    Args:
        project_id: Project ID
        
    Returns:
        Project information
        
    Raises:
        ValueError: If project not found
    """
    db = next(get_db())
    try:
        project = crud.project.get_project(db=db, project_id=project_id)
        
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
    finally:
        db.close()


def update_project_tool(
    project_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a project
    
    Args:
        project_id: Project ID to update
        name: New project name (optional)
        description: New project description (optional)
        
    Returns:
        Updated project information
        
    Raises:
        ValueError: If project not found
    """
    db = next(get_db())
    try:
        # Check if project exists
        existing_project = crud.project.get_project(db=db, project_id=project_id)
        if not existing_project:
            raise ValueError(f"Project not found: {project_id}")
        
        # Create update data
        update_data = ProjectUpdate()
        if name is not None:
            update_data.name = name
        if description is not None:
            update_data.description = description
        
        # Update project
        project = crud.project.update_project(
            db=db,
            project_id=project_id,
            project_update=update_data
        )
        
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
    finally:
        db.close()


def delete_project_tool(project_id: int) -> Dict[str, Any]:
    """
    Delete a project
    
    Args:
        project_id: Project ID to delete
        
    Returns:
        Deletion result
        
    Raises:
        ValueError: If project not found
    """
    db = next(get_db())
    try:
        # Check if project exists
        existing_project = crud.project.get_project(db=db, project_id=project_id)
        if not existing_project:
            raise ValueError(f"Project not found: {project_id}")
        
        # Delete project
        success = crud.project.delete_project(db=db, project_id=project_id)
        
        return {
            "success": success,
            "message": f"Project {project_id} deleted successfully" if success else f"Failed to delete project {project_id}"
        }
    finally:
        db.close() 