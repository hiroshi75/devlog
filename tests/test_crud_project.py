"""
プロジェクトCRUD操作のテスト
"""
import pytest
from sqlalchemy.orm import Session
from app.crud import project as crud_project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.project import Project


class TestProjectCRUD:
    """プロジェクトCRUD操作のテストクラス"""

    def test_get_project_by_id(self, db: Session):
        """IDによるプロジェクト取得のテスト"""
        # Arrange
        project = Project(name="Test Project", description="Test Description")
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # Act
        result = crud_project.get_project(db, project_id=project.id)
        
        # Assert
        assert result is not None
        assert result.id == project.id
        assert result.name == "Test Project"
        assert result.description == "Test Description"

    def test_get_project_not_found(self, db: Session):
        """存在しないプロジェクトの取得テスト"""
        # Act
        result = crud_project.get_project(db, project_id=999)
        
        # Assert
        assert result is None

    def test_get_projects_empty(self, db: Session):
        """プロジェクトリストの取得（空の場合）"""
        # Act
        result = crud_project.get_projects(db)
        
        # Assert
        assert result == []

    def test_get_projects_with_data(self, db: Session):
        """プロジェクトリストの取得（データあり）"""
        # Arrange
        project1 = Project(name="Project 1", description="Description 1")
        project2 = Project(name="Project 2", description="Description 2")
        db.add_all([project1, project2])
        db.commit()
        
        # Act
        result = crud_project.get_projects(db)
        
        # Assert
        assert len(result) == 2
        assert result[0].name == "Project 1"
        assert result[1].name == "Project 2"

    def test_get_projects_with_pagination(self, db: Session):
        """ページネーション付きプロジェクトリストの取得"""
        # Arrange
        for i in range(5):
            project = Project(name=f"Project {i}", description=f"Description {i}")
            db.add(project)
        db.commit()
        
        # Act
        result = crud_project.get_projects(db, skip=1, limit=2)
        
        # Assert
        assert len(result) == 2
        assert result[0].name == "Project 1"
        assert result[1].name == "Project 2"

    def test_create_project(self, db: Session):
        """プロジェクトの作成テスト"""
        # Arrange
        project_data = ProjectCreate(
            name="New Project",
            description="New Description"
        )
        
        # Act
        result = crud_project.create_project(db, project=project_data)
        
        # Assert
        assert result.id is not None
        assert result.name == "New Project"
        assert result.description == "New Description"
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_update_project(self, db: Session):
        """プロジェクトの更新テスト"""
        # Arrange
        project = Project(name="Original Name", description="Original Description")
        db.add(project)
        db.commit()
        db.refresh(project)
        
        update_data = ProjectUpdate(
            name="Updated Name",
            description="Updated Description"
        )
        
        # Act
        result = crud_project.update_project(db, project_id=project.id, project=update_data)
        
        # Assert
        assert result is not None
        assert result.name == "Updated Name"
        assert result.description == "Updated Description"
        assert result.updated_at > project.created_at

    def test_update_project_partial(self, db: Session):
        """プロジェクトの部分更新テスト"""
        # Arrange
        project = Project(name="Original Name", description="Original Description")
        db.add(project)
        db.commit()
        db.refresh(project)
        
        update_data = ProjectUpdate(name="Updated Name")
        
        # Act
        result = crud_project.update_project(db, project_id=project.id, project=update_data)
        
        # Assert
        assert result is not None
        assert result.name == "Updated Name"
        assert result.description == "Original Description"  # 変更されていない

    def test_update_project_not_found(self, db: Session):
        """存在しないプロジェクトの更新テスト"""
        # Arrange
        update_data = ProjectUpdate(name="Updated Name")
        
        # Act
        result = crud_project.update_project(db, project_id=999, project=update_data)
        
        # Assert
        assert result is None

    def test_delete_project(self, db: Session):
        """プロジェクトの削除テスト"""
        # Arrange
        project = Project(name="To Delete", description="Will be deleted")
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = project.id
        
        # Act
        result = crud_project.delete_project(db, project_id=project_id)
        
        # Assert
        assert result is True
        assert crud_project.get_project(db, project_id=project_id) is None

    def test_delete_project_not_found(self, db: Session):
        """存在しないプロジェクトの削除テスト"""
        # Act
        result = crud_project.delete_project(db, project_id=999)
        
        # Assert
        assert result is False 