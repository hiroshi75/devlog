"""
Project-related MCP resources for DevStatusMCP
"""

from typing import Dict, Any, Optional

from app.db.database import get_db
from app.models.project import Project as ProjectModel
from app import crud


def project_resource_handler(
    project_id: Any,
    include_tasks: bool = False
) -> Dict[str, Any]:
    """
    Handle project resource requests
    
    Args:
        project_id: Project ID to retrieve
        include_tasks: Whether to include related tasks (optional)
        
    Returns:
        Project information as dictionary
        
    Raises:
        ValueError: If project ID is invalid or project not found
    """
    # Validate project_id
    try:
        project_id = int(project_id)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid project ID: {project_id}")
    
    db = next(get_db())
    try:
        # Get project
        project = crud.project.get_project(db=db, project_id=project_id)
        
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        
        # Build response
        result = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
        
        # Include tasks if requested
        if include_tasks:
            tasks = crud.task.get_tasks(db=db, project_id=project_id)
            result["tasks"] = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "assignee_id": task.assignee_id,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
                for task in tasks
            ]
        
        return result
    finally:
        db.close() 