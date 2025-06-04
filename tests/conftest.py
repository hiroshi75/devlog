"""
テスト用の共通設定とフィクスチャ
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
# from app.main import app  # まだ作成されていないため一時的にコメントアウト

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


# @pytest.fixture
# def client(db):
#     """テスト用のFastAPIクライアント"""
#     def override_get_db():
#         try:
#             yield db
#         finally:
#             pass
#     
#     app.dependency_overrides[get_db] = override_get_db
#     
#     from fastapi.testclient import TestClient
#     with TestClient(app) as test_client:
#         yield test_client
#     
#     app.dependency_overrides.clear() 