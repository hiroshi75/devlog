"""
データベース接続設定

このモジュールは、SQLAlchemyを使用したデータベース接続の設定を提供します。
環境変数からデータベースURLを読み込み、適切なエンジンとセッションを設定します。
"""
import os
from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# データベースURLを環境変数から取得（デフォルトはSQLite）
SQLALCHEMY_DATABASE_URL: str = os.getenv(
    "DEVLOG_DATABASE_URL",
    "sqlite:///./devlog.db"
)

# SQLiteの場合の接続設定
connect_args: dict = {}
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    # SQLiteはマルチスレッドでの同一接続の使用を許可しない
    # FastAPIは非同期で動作するため、この設定が必要
    connect_args = {"check_same_thread": False}

# SQLAlchemyエンジンの作成
engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    # 開発環境ではSQLログを出力（本番環境では無効化すること）
    echo=bool(os.getenv("DEVLOG_DEBUG", False))
)

# セッションファクトリの作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    """
    全てのモデルの基底クラス
    
    このクラスを継承することで、SQLAlchemyのORMモデルを定義できます。
    各モデルは__tablename__属性を定義する必要があります。
    """
    pass


def get_db() -> Generator[Session, None, None]:
    """
    データベースセッションを取得する依存関数
    
    FastAPIの依存性注入システムで使用されます。
    リクエストごとに新しいセッションを作成し、
    リクエスト終了時に自動的にクローズします。
    
    Yields:
        Session: データベースセッション
    
    Example:
        ```python
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    データベースの初期化
    
    全てのモデルのテーブルを作成します。
    アプリケーション起動時に実行されます。
    
    Note:
        本番環境では、Alembicマイグレーションを使用することを推奨します。
        この関数は開発環境やテスト環境での利用を想定しています。
    """
    from app.models import project, task, user, message  # Import all models
    Base.metadata.create_all(bind=engine) 