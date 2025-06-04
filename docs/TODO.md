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

- [ ] `app/db/database.py` の作成
  - [ ] SQLAlchemy エンジンの設定
  - [ ] SessionLocal の作成
  - [ ] Base クラスの定義
  - [ ] get_db 依存関数の実装

### モデル定義

- [ ] `app/models/__init__.py` の作成
- [ ] `app/models/project.py` の作成
  - [ ] Project モデルの定義（id, name, description, created_at, updated_at）
- [ ] `app/models/task.py` の作成
  - [ ] Task モデルの定義（id, title, description, status, project_id, assignee_id, created_at, updated_at）
- [ ] `app/models/user.py` の作成
  - [ ] User モデルの定義（id, username, email, created_at）
- [ ] `app/models/message.py` の作成
  - [ ] Message モデルの定義（id, content, message_type, user_id, task_id, project_id, parent_id, created_at）

### Alembic 設定

- [ ] Alembic の初期化 (`alembic init alembic`)
- [ ] `alembic.ini` の設定
- [ ] `alembic/env.py` の設定
- [ ] 初期マイグレーションの作成
- [ ] マイグレーションの実行

## 📋 スキーマ定義

### Pydantic スキーマ

- [ ] `app/schemas/__init__.py` の作成
- [ ] `app/schemas/project.py` の作成
  - [ ] ProjectBase スキーマ
  - [ ] ProjectCreate スキーマ
  - [ ] ProjectUpdate スキーマ
  - [ ] Project レスポンススキーマ
- [ ] `app/schemas/task.py` の作成
  - [ ] TaskBase スキーマ
  - [ ] TaskCreate スキーマ
  - [ ] TaskUpdate スキーマ
  - [ ] Task レスポンススキーマ
- [ ] `app/schemas/user.py` の作成
  - [ ] UserBase スキーマ
  - [ ] UserCreate スキーマ
  - [ ] User レスポンススキーマ
- [ ] `app/schemas/message.py` の作成
  - [ ] MessageBase スキーマ
  - [ ] MessageCreate スキーマ
  - [ ] Message レスポンススキーマ

## 🔧 CRUD 操作

### CRUD 実装

- [ ] `app/crud/__init__.py` の作成
- [ ] `app/crud/project.py` の作成
  - [ ] get_project 関数
  - [ ] get_projects 関数
  - [ ] create_project 関数
  - [ ] update_project 関数
  - [ ] delete_project 関数
- [ ] `app/crud/task.py` の作成
  - [ ] get_task 関数
  - [ ] get_tasks 関数
  - [ ] create_task 関数
  - [ ] update_task 関数
  - [ ] delete_task 関数
- [ ] `app/crud/user.py` の作成
  - [ ] get_user 関数
  - [ ] get_users 関数
  - [ ] create_user 関数
- [ ] `app/crud/message.py` の作成
  - [ ] get_message 関数
  - [ ] get_messages 関数
  - [ ] create_message 関数

## 🌐 API エンドポイント

### ルーター実装

- [ ] `app/api/__init__.py` の作成
- [ ] `app/api/projects.py` の作成
  - [ ] GET `/projects/` エンドポイント
  - [ ] POST `/projects/` エンドポイント
  - [ ] GET `/projects/{id}` エンドポイント
  - [ ] PUT `/projects/{id}` エンドポイント
  - [ ] DELETE `/projects/{id}` エンドポイント
- [ ] `app/api/tasks.py` の作成
  - [ ] GET `/tasks/` エンドポイント
  - [ ] POST `/tasks/` エンドポイント
  - [ ] GET `/tasks/{id}` エンドポイント
  - [ ] PUT `/tasks/{id}` エンドポイント
  - [ ] DELETE `/tasks/{id}` エンドポイント
- [ ] `app/api/users.py` の作成
  - [ ] GET `/users/` エンドポイント
  - [ ] POST `/users/` エンドポイント
  - [ ] GET `/users/{id}` エンドポイント
- [ ] `app/api/messages.py` の作成
  - [ ] GET `/messages/` エンドポイント（フィルター対応）
  - [ ] POST `/messages/` エンドポイント
  - [ ] GET `/messages/{id}` エンドポイント

### メインアプリケーション

- [ ] `app/main.py` の作成
  - [ ] FastAPI アプリケーションの初期化
  - [ ] ルーターの登録
  - [ ] CORS 設定（必要に応じて）
  - [ ] ヘルスチェックエンドポイント

## 🧪 テスト

### テスト環境設定

- [ ] `tests/__init__.py` の作成
- [ ] `tests/conftest.py` の作成
  - [ ] テスト用データベースの設定
  - [ ] テストクライアントの設定
  - [ ] フィクスチャの定義

### 単体テスト

- [ ] `tests/test_models.py` の作成
  - [ ] Project モデルのテスト
  - [ ] Task モデルのテスト
  - [ ] User モデルのテスト
  - [ ] Message モデルのテスト

### 統合テスト

- [ ] `tests/test_api_projects.py` の作成
  - [ ] プロジェクト CRUD のテスト
- [ ] `tests/test_api_tasks.py` の作成
  - [ ] タスク CRUD のテスト
- [ ] `tests/test_api_users.py` の作成
  - [ ] ユーザー CRUD のテスト
- [ ] `tests/test_api_messages.py` の作成
  - [ ] メッセージ CRUD のテスト

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
