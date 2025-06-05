# DevStatusMCP 開発 TODO

## 🏗️ プロジェクト初期設定

### 環境構築

- [x] プロジェクトディレクトリ構造の作成
  - [x] `app/` ディレクトリ作成
  - [x] `app/models/` ディレクトリ作成
  - [x] `app/schemas/` ディレクトリ作成
  - [x] `app/crud/` ディレクトリ作成
  - [x] `app/tools/` ディレクトリ作成（MCP ツール用）
  - [x] `app/resources/` ディレクトリ作成（MCP リソース用）
  - [x] `app/db/` ディレクトリ作成
  - [x] `tests/` ディレクトリ作成
  - [x] `alembic/` ディレクトリ作成

### 依存関係のセットアップ

- [x] 必要なライブラリのインストール
  - [x] FastMCP のインストール (`uv add fastmcp`)
  - [x] SQLAlchemy のインストール (`uv add sqlalchemy`)
  - [x] Alembic のインストール (`uv add alembic`)
  - [x] Pydantic のインストール (`uv add pydantic`)
  - [x] python-dotenv のインストール (`uv add python-dotenv`)
  - [x] psycopg2-binary のインストール (`uv add psycopg2-binary`)
  - [x] pytest のインストール (`uv add pytest`)
  - [x] pytest-asyncio のインストール (`uv add pytest-asyncio`)

## 🗄️ データベース設計

### データベース接続設定

- [x] `app/db/database.py` の作成
  - [x] SQLAlchemy エンジンの設定
  - [x] SessionLocal の作成
  - [x] Base クラスの定義
  - [x] get_db 依存関数の実装
  - [x] init_db 関数の実装

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

## 🛠️ MCP サーバー実装

### MCP ツール実装

- [x] `app/tools/__init__.py` の作成
- [x] `app/tools/project_tools.py` の作成
  - [x] create_project ツール
  - [x] get_projects ツール
  - [x] get_project ツール
  - [x] update_project ツール
  - [x] delete_project ツール
- [x] `app/tools/task_tools.py` の作成
  - [x] create_task ツール
  - [x] get_tasks ツール
  - [x] get_task ツール
  - [x] update_task ツール
  - [x] delete_task ツール
- [x] `app/tools/user_tools.py` の作成
  - [x] create_user ツール
  - [x] get_users ツール
  - [x] get_user ツール
- [x] `app/tools/message_tools.py` の作成
  - [x] create_message ツール
  - [x] get_messages ツール
  - [x] get_message ツール

### MCP リソース実装

- [x] `app/resources/__init__.py` の作成
- [x] `app/resources/project_resources.py` の作成
  - [x] project://{project_id} リソース
- [x] `app/resources/task_resources.py` の作成
  - [x] task://{task_id} リソース
- [x] `app/resources/user_resources.py` の作成
  - [x] user://{user_id} リソース
- [x] `app/resources/message_resources.py` の作成
  - [x] messages://{type} リソース（recent 対応）

### メインアプリケーション

- [x] `app/main.py` の作成
  - [x] FastMCP サーバーの初期化
  - [x] ツールの登録（16 個のツール）
  - [x] リソースの登録（4 個のリソース）
  - [x] データベース接続の設定
  - [x] サーバー起動設定

## 🧪 テスト

### テスト環境設定

- [x] `tests/__init__.py` の作成
- [x] `tests/conftest.py` の作成
  - [x] テスト用データベースの設定
  - [x] MCP クライアント（モック）の設定
  - [x] フィクスチャの定義

### 単体テスト

- [x] `tests/test_models.py` の作成
  - [x] Project モデルのテスト
  - [x] Task モデルのテスト
  - [x] User モデルのテスト
  - [x] Message モデルのテスト

### MCP ツールテスト

- [x] `tests/test_project_tools.py` の作成
  - [x] プロジェクト関連ツールのテスト
- [x] `tests/test_task_tools.py` の作成
  - [x] タスク関連ツールのテスト
- [x] `tests/test_user_tools.py` の作成
  - [x] ユーザー関連ツールのテスト
- [x] `tests/test_message_tools.py` の作成
  - [x] メッセージ関連ツールのテスト

### MCP リソーステスト

- [x] `tests/test_project_resources.py` の作成
  - [x] プロジェクトリソースのテスト
- [x] `tests/test_task_resources.py` の作成
  - [x] タスクリソースのテスト
- [x] `tests/test_user_resources.py` の作成
  - [x] ユーザーリソースのテスト
- [x] `tests/test_message_resources.py` の作成
  - [x] メッセージリソースのテスト

### メインアプリケーションテスト

- [x] `tests/test_main.py` の作成
  - [x] FastMCP サーバーの初期化テスト
  - [x] ツール登録の確認テスト
  - [x] リソース登録の確認テスト
  - [x] ツール機能のテスト
  - [x] リソース機能のテスト

## 📚 ドキュメント

### MCP サーバー仕様書

- [x] FastMCP 基本ガイドの作成
- [x] ツール一覧と使用例の作成 (`docs/tools_guide.md`)
- [x] リソース一覧と使用例の作成 (`docs/resources_guide.md`)
- [x] Claude Desktop / Cursor での設定手順 (`docs/setup_guide.md`)

### 開発ドキュメント

- [x] 環境構築手順の詳細化 (`docs/setup_guide.md` に含まれる)
- [ ] デプロイ手順の作成
- [ ] トラブルシューティングガイド (`docs/setup_guide.md` に基本的な内容を含む)

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
- [ ] プロンプトテンプレートの追加
- [ ] 高度なフィルタリング機能
- [ ] 統計情報の提供
- [ ] バッチ操作のサポート
- [ ] WebSocket 対応（リアルタイム更新）

---

## 進捗管理のルール

1. 各タスクは完了したらチェックボックスにチェックを入れる
2. 新しい課題が見つかったら、適切なセクションに追加する
3. 優先度の高いタスクから順に実施する
4. テストは各機能実装前に必ず作成する（TDD 推奨）

---

## 🎉 現在の状況

**FastMCP サーバーの実装が完了しました！**

- ✅ 16 個の MCP ツールが登録済み
- ✅ 4 個の MCP リソースが登録済み
- ✅ TDD に基づく全テストが通過
- ✅ データベース接続と CRUD 操作が動作
- ✅ FastMCP サーバーが正常に起動可能

次のステップ: ドキュメント作成またはデプロイ準備
