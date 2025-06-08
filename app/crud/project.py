"""
プロジェクトのCRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int) -> Optional[Project]:
    """IDによるプロジェクトの取得"""
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    """プロジェクトリストの取得"""
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: ProjectCreate) -> Project:
    """プロジェクトの作成"""
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(
    db: Session, project_id: int, project: ProjectUpdate
) -> Optional[Project]:
    """プロジェクトの更新"""
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        return None
    
    update_data = project.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    """プロジェクトの削除"""
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        return False
    
    # 関連するタスクを削除
    from app.models.task import Task
    db.query(Task).filter(Task.project_id == project_id).delete()
    
    # 関連するメッセージのproject_idをNullに設定
    from app.models.message import Message
    db.query(Message).filter(Message.project_id == project_id).update({"project_id": None})
    
    # プロジェクトを削除
    db.delete(db_project)
    db.commit()
    return True 