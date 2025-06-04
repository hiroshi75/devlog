"""
Projectスキーマのテスト

ProjectBase, ProjectCreate, ProjectUpdate, Projectスキーマの
バリデーションと動作をテストします。
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.project import ProjectBase, ProjectCreate, ProjectUpdate, Project


class TestProjectBase:
    """ProjectBaseスキーマのテスト"""
    
    def test_valid_project_base(self):
        """有効なProjectBaseの作成"""
        project = ProjectBase(
            name="Test Project",
            description="This is a test project"
        )
        assert project.name == "Test Project"
        assert project.description == "This is a test project"
    
    def test_project_base_without_description(self):
        """説明なしのProjectBase"""
        project = ProjectBase(name="Test Project")
        assert project.name == "Test Project"
        assert project.description is None
    
    def test_project_base_empty_name(self):
        """空の名前でエラー"""
        with pytest.raises(ValidationError):
            ProjectBase(name="", description="Test")
    
    def test_project_base_missing_name(self):
        """名前なしでエラー"""
        with pytest.raises(ValidationError):
            ProjectBase(description="Test")


class TestProjectCreate:
    """ProjectCreateスキーマのテスト"""
    
    def test_valid_project_create(self):
        """有効なProjectCreateの作成"""
        project = ProjectCreate(
            name="New Project",
            description="Creating a new project"
        )
        assert project.name == "New Project"
        assert project.description == "Creating a new project"
    
    def test_project_create_inherits_from_base(self):
        """ProjectBaseを継承していることを確認"""
        assert issubclass(ProjectCreate, ProjectBase)


class TestProjectUpdate:
    """ProjectUpdateスキーマのテスト"""
    
    def test_update_all_fields(self):
        """全フィールドの更新"""
        update = ProjectUpdate(
            name="Updated Project",
            description="Updated description"
        )
        assert update.name == "Updated Project"
        assert update.description == "Updated description"
    
    def test_update_name_only(self):
        """名前のみ更新"""
        update = ProjectUpdate(name="Updated Name")
        assert update.name == "Updated Name"
        assert update.description is None
    
    def test_update_description_only(self):
        """説明のみ更新"""
        update = ProjectUpdate(description="Updated description")
        assert update.name is None
        assert update.description == "Updated description"
    
    def test_empty_update(self):
        """空の更新（全フィールドがオプション）"""
        update = ProjectUpdate()
        assert update.name is None
        assert update.description is None


class TestProject:
    """Projectレスポンススキーマのテスト"""
    
    def test_valid_project_response(self):
        """有効なProjectレスポンスの作成"""
        now = datetime.now()
        project = Project(
            id=1,
            name="Test Project",
            description="Test description",
            created_at=now,
            updated_at=now
        )
        assert project.id == 1
        assert project.name == "Test Project"
        assert project.description == "Test description"
        assert project.created_at == now
        assert project.updated_at == now
    
    def test_project_inherits_from_base(self):
        """ProjectBaseを継承していることを確認"""
        assert issubclass(Project, ProjectBase)
    
    def test_project_from_orm_mode(self):
        """ORMモードが有効であることを確認"""
        # ConfigクラスでORMモードが設定されていることを確認
        assert hasattr(Project, 'model_config')
        assert Project.model_config.get('from_attributes', False) is True 