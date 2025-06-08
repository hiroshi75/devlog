# DevLog

Slack 風の開発状況共有サービスのための MCP（Model Context Protocol）サーバーです。  
複数人が複数プロジェクトで複数タスクを進める状況において、開発進捗やコメントなどをメッセージ形式で一元管理し、LLM と連携して開発状況を把握・管理することを目的としています。

## 📦 機能概要

- プロジェクトの作成・取得・更新・削除
- タスクの作成・取得・更新・削除
- ユーザー管理（追加・一覧取得）
- メッセージ投稿・取得（ステータス更新、スレッド対応）
- LLM との統合による自然言語での操作

## 🚀 使用技術

- Python 3.12+
- FastMCP（MCP サーバーフレームワーク）
- SQLAlchemy
- PostgreSQL（または SQLite for development）
- Alembic（マイグレーション）

---

## 🛠️ セットアップ手順

### 1. 依存関係のインストール

```bash
# uvを使用（推奨）
uv sync

# または pip を使用
pip install -e .
```

新規に依存関係を追加する場合：

```bash
uv add パッケージ名
```

### 2. .env ファイルの作成

`.env` ファイルに以下のような内容を記述してください：

```env
DEVLOG_DATABASE_URL=postgresql://user:password@localhost/devstatus
```

※ SQLite を使う場合は：

```env
DEVLOG_DATABASE_URL=sqlite:///./devstatus.db
```

### 3. データベース初期化

```bash
alembic upgrade head
```

---

## ▶️ 実行方法

### MCP サーバーとして実行

```bash
# 標準実行（STDIO トランスポート）
python app/main.py

# FastMCP CLI を使用
fastmcp run app/main.py:mcp

# デバッグモード
fastmcp run app/main.py:mcp --log-level DEBUG
```

### MCP インスペクターでテスト

```bash
mcp dev app/main.py
```

ブラウザで [http://localhost:5173](http://localhost:5173) にアクセスして、ツールやリソースをテストできます。

---

## 🔧 MCP ツール一覧

### プロジェクト管理

- `create_project` - 新規プロジェクトを作成
- `get_projects` - プロジェクト一覧を取得
- `get_project` - 特定のプロジェクトを取得
- `update_project` - プロジェクト情報を更新
- `delete_project` - プロジェクトを削除

### タスク管理

- `create_task` - 新規タスクを作成
- `get_tasks` - タスク一覧を取得（プロジェクトやステータスでフィルタ可能）
- `get_task` - 特定のタスクを取得
- `update_task` - タスク情報を更新
- `delete_task` - タスクを削除

### ユーザー管理

- `create_user` - 新規ユーザーを登録
- `get_users` - ユーザー一覧を取得
- `get_user` - 特定のユーザー情報を取得

### メッセージ管理

- `create_message` - メッセージを投稿
- `get_messages` - メッセージ一覧を取得（各種フィルタ対応）
- `get_message` - 特定のメッセージを取得

---

## 📋 MCP リソース一覧

- `project://{project_id}` - プロジェクト情報
- `task://{task_id}` - タスク情報
- `user://{user_id}` - ユーザー情報
- `messages://recent` - 最近のメッセージ一覧

---

## 🤖 Claude Desktop / Cursor での使用

### Claude Desktop へのインストール

```bash
fastmcp install app/main.py
```

### Cursor での設定

`~/.cursor/mcp.json` に以下を追加：

```json
{
  "mcpServers": {
    "devstatus": {
      "command": "uv",
      "args": ["--directory", "/path/to/devlog", "run", "app/main.py"]
    }
  }
}
```

---

## 📂 ディレクトリ構成

```
devlog/
├── app/
│   ├── main.py           # FastMCPサーバーのエントリーポイント
│   ├── models/           # SQLAlchemyモデル
│   ├── schemas/          # Pydanticスキーマ
│   ├── crud/             # CRUD操作ロジック
│   ├── tools/            # MCPツール定義
│   ├── resources/        # MCPリソース定義
│   ├── api/              # API関連コード
│   └── db/               # DB接続・初期化
├── tests/                # テストコード
├── alembic/              # マイグレーション管理
├── docs/                 # ドキュメント
│   ├── TODO.md          # 開発タスク管理
│   └── fastmcp_guide.md # FastMCP基本ガイド
├── pyproject.toml        # プロジェクト設定・依存関係
├── uv.lock               # 依存関係ロックファイル
└── README.md
```

---

## 🧪 テスト

TDD（テスト駆動開発）で実装を進めています：

```bash
# テストの実行
uv run pytest

# 詳細な出力でテスト実行
uv run pytest -v

# カバレッジ付きテスト
uv run pytest --cov=app --cov-report=html

# 特定のテストファイルのみ実行
uv run pytest tests/test_models.py

# 特定のテストクラスのみ実行
uv run pytest tests/test_models.py::TestProjectModel

# 特定のテスト関数のみ実行
uv run pytest tests/test_models.py::TestProjectModel::test_create_project_success
```

---

## 📝 ライセンス

MIT License
