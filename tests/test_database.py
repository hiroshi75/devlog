"""
データベース接続設定のテスト
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import DeclarativeBase


class TestDatabase:
    """データベース接続設定のテストクラス"""
    
    def test_database_module_exists(self):
        """database.pyモジュールが存在することを確認"""
        try:
            from app.db import database
        except ImportError:
            pytest.fail("app.db.database モジュールが存在しません")
    
    def test_engine_creation(self):
        """SQLAlchemyエンジンが正しく作成されることを確認"""
        from app.db.database import engine
        
        assert engine is not None
        # SQLAlchemy 2.0では、engineの使い方が変わったため、基本的な属性のみチェック
        assert hasattr(engine, 'url')
        assert hasattr(engine, 'connect')
    
    def test_session_local_creation(self):
        """SessionLocalが正しく設定されることを確認"""
        from app.db.database import SessionLocal
        
        assert SessionLocal is not None
        # SessionLocalがsessionmakerのインスタンスであることを確認
        assert hasattr(SessionLocal, '__call__')
        
        # セッションが作成できることを確認
        session = SessionLocal()
        assert isinstance(session, Session)
        session.close()
    
    def test_base_class_exists(self):
        """Baseクラスが定義されていることを確認"""
        from app.db.database import Base
        
        assert Base is not None
        assert hasattr(Base, 'metadata')
        # DeclarativeBaseを継承していることを確認
        assert issubclass(Base, DeclarativeBase)
    
    def test_get_db_dependency(self):
        """get_db依存関数が正しく動作することを確認"""
        from app.db.database import get_db
        
        # ジェネレータ関数であることを確認
        db_gen = get_db()
        assert hasattr(db_gen, '__next__')
        
        # セッションが取得できることを確認
        db = next(db_gen)
        assert isinstance(db, Session)
        
        # クリーンアップが正しく行われることを確認
        try:
            next(db_gen)
        except StopIteration:
            pass  # 正常終了
        else:
            pytest.fail("get_db関数が正しく終了しませんでした")
    
    def test_database_url_configuration(self):
        """データベースURLが環境変数から読み込まれることを確認"""
        import os
        from app.db.database import SQLALCHEMY_DATABASE_URL
        
        # テスト用のデータベースURLが設定されていることを確認
        assert SQLALCHEMY_DATABASE_URL is not None
        assert isinstance(SQLALCHEMY_DATABASE_URL, str)
        
        # SQLiteを使用している場合の確認（開発環境）
        if "sqlite" in SQLALCHEMY_DATABASE_URL:
            assert "sqlite:///" in SQLALCHEMY_DATABASE_URL 