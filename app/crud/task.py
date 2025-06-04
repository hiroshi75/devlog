"""
タスクのCRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """IDによるタスクの取得"""
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[Task]:
    """タスクリストの取得"""
    query = db.query(Task)
    
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    
    if status is not None:
        query = query.filter(Task.status == status)
    
    return query.offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate) -> Task:
    """タスクの作成"""
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session, task_id: int, task: TaskUpdate
) -> Optional[Task]:
    """タスクの更新"""
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        return None
    
    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """タスクの削除"""
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        return False
    
    db.delete(db_task)
    db.commit()
    return True 