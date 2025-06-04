"""
Project API endpoints
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import project as crud_project
from app.db.database import get_db
from app.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter()


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project"""
    return crud_project.create_project(db=db, project=project)


@router.get("/", response_model=List[Project])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all projects"""
    projects = crud_project.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=Project)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project by ID"""
    db_project = crud_project.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a project"""
    db_project = crud_project.update_project(
        db=db,
        project_id=project_id,
        project=project
    )
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project"""
    success = crud_project.delete_project(db=db, project_id=project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return None 