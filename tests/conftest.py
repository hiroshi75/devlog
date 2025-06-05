"""
テスト用の共通設定とフィクスチャ
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db

# すべてのモデルをインポートして、リレーションシップが正しく解決されるようにする
from app.models import Project, Task, User, Message  # noqa: F401


# テスト用のSQLiteデータベースを使用
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """テスト用のデータベースセッション"""
    # テーブルの作成
    Base.metadata.create_all(bind=engine)
    
    # セッションの作成
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # テーブルの削除
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mcp_client(db):
    """テスト用のMCPクライアント（モック）"""
    # Override database dependency for testing
    import app.tools.project_tools
    import app.tools.task_tools
    import app.tools.user_tools
    import app.tools.message_tools
    
    # Mock the get_db function in all tool modules
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    # Override get_db in all modules that use it
    original_get_db = get_db
    app.tools.project_tools.get_db = lambda: [db]
    app.tools.task_tools.get_db = lambda: [db]
    app.tools.user_tools.get_db = lambda: [db]
    app.tools.message_tools.get_db = lambda: [db]
    
    try:
        yield db  # Return db session for direct testing
    finally:
        # Restore original get_db function
        app.tools.project_tools.get_db = original_get_db
        app.tools.task_tools.get_db = original_get_db
        app.tools.user_tools.get_db = original_get_db
        app.tools.message_tools.get_db = original_get_db 