# DevStatusAPI 開発 TODO

## 🏗️ プロジェクト初期設定

### 環境構築

- [x] プロジェクトディレクトリ構造の作成
  - [x] `app/` ディレクトリ作成
  - [x] `app/models/` ディレクトリ作成
  - [x] `app/schemas/` ディレクトリ作成
  - [x] `app/crud/` ディレクトリ作成
  - [x] `app/api/` ディレクトリ作成
  - [x] `app/db/` ディレクトリ作成
  - [x] `tests/` ディレクトリ作成
  - [x] `alembic/` ディレクトリ作成

### 依存関係のセットアップ

- [x] 必要なライブラリのインストール
  - [x] FastAPI のインストール (`uv add fastapi`)
  - [x] SQLAlchemy のインストール (`uv add sqlalchemy`)
  - [x] Alembic のインストール (`uv add alembic`)
  - [x] Uvicorn のインストール (`uv add uvicorn`)
  - [x] Pydantic のインストール (`uv add pydantic`)
  - [x] python-dotenv のインストール (`uv add python-dotenv`)
  - [x] psycopg2-binary のインストール (`uv add psycopg2-binary`)
  - [x] pytest のインストール (`uv add pytest`)
  - [x] httpx のインストール (テスト用) (`uv add httpx`)

## 🗄️ データベース設計

### データベース接続設定

- [x] `app/db/database.py` の作成
  - [x] SQLAlchemy エンジンの設定
  - [x] SessionLocal の作成
  - [x] Base クラスの定義
  - [x] get_db 依存関数の実装

### モデル定義

- [x] `app/models/__init__.py` の作成
- [x] `app/models/project.py` の作成
  - [x] Project モデルの定義（id, name, description, created_at, updated_at）
- [x] `app/models/task.py` の作成
  - [x] Task モデルの定義（id, title, description, status, project_id, assignee_id, created_at, updated_at）
- [x] `app/models/user.py` の作成
  - [x] User モデルの定義（id, username, email, created_at）
- [x] `app/models/message.py` の作成
  - [x] Message モデルの定義（id, content, message_type, user_id, task_id, project_id, parent_id, created_at）

### Alembic 設定

- [x] Alembic の初期化 (`alembic init alembic`)
- [x] `alembic.ini` の設定
- [x] `alembic/env.py` の設定
- [x] 初期マイグレーションの作成
- [x] マイグレーションの実行

## 📋 スキーマ定義

### Pydantic スキーマ

- [x] `app/schemas/__init__.py` の作成
- [x] `app/schemas/project.py` の作成
  - [x] ProjectBase スキーマ
  - [x] ProjectCreate スキーマ
  - [x] ProjectUpdate スキーマ
  - [x] Project レスポンススキーマ
- [x] `app/schemas/task.py` の作成
  - [x] TaskBase スキーマ
  - [x] TaskCreate スキーマ
  - [x] TaskUpdate スキーマ
  - [x] Task レスポンススキーマ
- [x] `app/schemas/user.py` の作成
  - [x] UserBase スキーマ
  - [x] UserCreate スキーマ
  - [x] User レスポンススキーマ
- [x] `app/schemas/message.py` の作成
  - [x] MessageBase スキーマ
  - [x] MessageCreate スキーマ
  - [x] Message レスポンススキーマ

## 🔧 CRUD 操作

### CRUD 実装

- [x] `app/crud/__init__.py` の作成
- [x] `app/crud/project.py` の作成
  - [x] get_project 関数
  - [x] get_projects 関数
  - [x] create_project 関数
  - [x] update_project 関数
  - [x] delete_project 関数
- [x] `app/crud/task.py` の作成
  - [x] get_task 関数
  - [x] get_tasks 関数
  - [x] create_task 関数
  - [x] update_task 関数
  - [x] delete_task 関数
- [x] `app/crud/user.py` の作成
  - [x] get_user 関数
  - [x] get_users 関数
  - [x] create_user 関数
- [x] `app/crud/message.py` の作成
  - [x] get_message 関数
  - [x] get_messages 関数
  - [x] create_message 関数

## 🌐 API エンドポイント

### ルーター実装

- [x] `app/api/__init__.py` の作成
- [x] `app/api/projects.py` の作成
  - [x] GET `/projects/` エンドポイント
  - [x] POST `/projects/` エンドポイント
  - [x] GET `/projects/{id}` エンドポイント
  - [x] PUT `/projects/{id}` エンドポイント
  - [x] DELETE `/projects/{id}` エンドポイント
- [x] `app/api/tasks.py` の作成
  - [x] GET `/tasks/` エンドポイント
  - [x] POST `/tasks/` エンドポイント
  - [x] GET `/tasks/{id}` エンドポイント
  - [x] PUT `/tasks/{id}` エンドポイント
  - [x] DELETE `/tasks/{id}` エンドポイント
- [x] `app/api/users.py` の作成
  - [x] GET `/users/` エンドポイント
  - [x] POST `/users/` エンドポイント
  - [x] GET `/users/{id}` エンドポイント
- [x] `app/api/messages.py` の作成
  - [x] GET `/messages/` エンドポイント（フィルター対応）
  - [x] POST `/messages/` エンドポイント
  - [x] GET `/messages/{id}` エンドポイント

### メインアプリケーション

- [x] `app/main.py` の作成
  - [x] FastAPI アプリケーションの初期化
  - [x] ルーターの登録
  - [x] CORS 設定（必要に応じて）
  - [x] ヘルスチェックエンドポイント

## 🧪 テスト

### テスト環境設定

- [x] `tests/__init__.py` の作成
- [x] `tests/conftest.py` の作成
  - [x] テスト用データベースの設定
  - [x] テストクライアントの設定
  - [x] フィクスチャの定義

### 単体テスト

- [x] `tests/test_models.py` の作成
  - [x] Project モデルのテスト
  - [x] Task モデルのテスト
  - [x] User モデルのテスト
  - [x] Message モデルのテスト

### 統合テスト

- [x] `tests/test_api_projects.py` の作成
  - [x] プロジェクト CRUD のテスト
- [x] `tests/test_api_tasks.py` の作成
  - [x] タスク CRUD のテスト
- [x] `tests/test_api_users.py` の作成
  - [x] ユーザー CRUD のテスト
- [x] `tests/test_api_messages.py` の作成
  - [x] メッセージ CRUD のテスト

## 📚 ドキュメント

### API 仕様書

- [ ] OpenAPI 仕様の確認
- [ ] エンドポイントの説明追加
- [ ] リクエスト/レスポンス例の追加

### 開発ドキュメント

- [ ] 環境構築手順の詳細化
- [ ] デプロイ手順の作成
- [ ] トラブルシューティングガイド

## 🚀 デプロイ準備

### 本番環境設定

- [ ] 環境変数の管理方法確定
- [ ] ログ設定の実装
- [ ] エラーハンドリングの強化
- [ ] パフォーマンス最適化

### CI/CD

- [ ] GitHub Actions の設定（オプション）
- [ ] 自動テストの設定
- [ ] 自動デプロイの設定（オプション）

## 📝 追加機能（将来的な拡張）

- [ ] 認証・認可機能の実装
- [ ] WebSocket 対応（リアルタイム更新）
- [ ] ファイルアップロード機能
- [ ] 通知機能
- [ ] 検索機能の強化
- [ ] ダッシュボード機能

---

## 進捗管理のルール

1. 各タスクは完了したらチェックボックスにチェックを入れる
2. 新しい課題が見つかったら、適切なセクションに追加する
3. 優先度の高いタスクから順に実施する
4. テストは各機能実装後に必ず作成する（TDD 推奨）
