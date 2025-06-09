# DevLog

Slack 風の開発状況共有サービスのための MCP（Model Context Protocol）サーバーです。  
複数人が複数プロジェクトで複数タスクを進める状況において、開発進捗やコメントなどをメッセージ形式で一元管理し、LLM と連携して開発状況を把握・管理することを目的としています。

## 📦 機能概要

### 🗣️ Slack 風コミュニケーション機能

- **チャンネル型メッセージング**: プロジェクト・タスク単位でのグループコミュニケーション
- **ダイレクトメッセージ（DM）**: 1 対 1 の個人間コミュニケーション
- **スレッド機能**: メッセージへの返信でコンテキストを保持
- **既読管理**: 未読メッセージの把握と一括既読機能
- **メッセージタイプ**: コメント、質問、回答、アナウンス、タスク更新など

### 📋 プロジェクト・タスク管理

- プロジェクトの作成・取得・更新・削除
- タスクの作成・取得・更新・削除
- プロジェクト・タスクに紐づいたメッセージング

### 👥 ユーザー管理

- ユーザー登録・一覧取得
- ユーザー間のコミュニケーション機能

### 🤖 LLM 連携

- LLM との統合による自然言語での操作
- 開発状況の自動要約・分析

> 💻 **API の詳細**: [API リファレンス](docs/API.md) で全機能の使用方法をご確認ください。

## 🚀 使用技術

- Python 3.12+
- FastMCP（MCP サーバーフレームワーク）
- SQLAlchemy
- PostgreSQL（または SQLite for development）
- Alembic（マイグレーション）

---

## 💡 どんな場面で使える？

### チーム開発での状況共有

```
👨‍💻 田中: 「ユーザー認証機能が完了しました。テストも通っています」
👩‍💻 佐藤: └ 「お疲れ様です！次はAPI統合に取り掛かりますね」
🤖 AI: 「ユーザー認証完了により、全体の進捗率が65%になりました」
```

### 個人間の相談・質問

```
👨‍💻 新人: 「@シニア開発者さん、エラーで困っています。ちょっと相談できますか？」
👩‍💻 シニア: 「もちろんです！どんなエラーですか？」
```

### プロジェクト全体のアナウンス

```
👤 PM: 「【重要】リリース日が来週金曜日に決定しました。最終チェックをお願いします」
```

---

## 🛠️ セットアップ手順

### 1. 依存関係のインストール

```bash
# uvを使用（推奨）
uv sync
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
uv run alembic upgrade head
```

## 🤖 Claude Desktop / Cursor での使用

```json
{
  "mcpServers": {
    "devlog": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/devlog",
        "run",
        "--",
        "python",
        "app/main.py"
      ],
      "env": {
        "DEVLOG_DATABASE_URL": "sqlite:////path/to/devlog/devlog.db",
        "PYTHONPATH": "/path/to/devlog"
      }
    }
  }
}
```

---

## ▶️ 実行方法

### MCP サーバーとして実行

```bash
# 標準実行（STDIO トランスポート）
uv run python app/main.py

# FastMCP CLI を使用
uv run fastmcp run app/main.py:mcp

# デバッグモード
uv run fastmcp run app/main.py:mcp --log-level DEBUG
```

---

## 🔧 MCP ツール一覧

> 📖 **詳細な API リファレンス**: [docs/API.md](docs/API.md) で全ツールの詳細な使用方法、パラメータ、戻り値、使用例をご確認いただけます。

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

### 💬 メッセージ・コミュニケーション機能

#### 基本メッセージ機能

- `create_message` - メッセージを投稿（プロジェクト・タスク・DM・スレッド対応）
- `get_messages` - メッセージ一覧を取得（各種フィルタ対応）
- `get_message` - 特定のメッセージを取得

#### ダイレクトメッセージ（DM）

- `create_direct_message` - 1 対 1 のダイレクトメッセージを送信
- `get_direct_messages` - 2 ユーザー間の DM 履歴を取得

#### スレッド機能

- `get_thread_messages` - 特定メッセージへの返信（スレッド）を取得
- メッセージ作成時に`parent_id`を指定してスレッド返信

#### 既読管理

- `get_unread_messages` - 未読メッセージの一覧を取得
- `mark_message_as_read` - 特定メッセージを既読にする
- `mark_conversation_as_read` - 会話の全メッセージを一括既読

#### メッセージ管理

- `delete_message` - メッセージを削除（論理削除）

---

## 🎯 実際の使用例

### 1. プロジェクトでの進捗共有

```python
# プロジェクトの作成
create_project(name="ユーザー管理システム", description="新サービスのユーザー管理機能")

# タスクの作成
create_task(title="ログイン機能の実装", project_id=1, assignee_id=1)

# 進捗をプロジェクトに投稿
create_message(
    content="ログイン機能のフロントエンド部分が完了しました。テスト中です。",
    user_id=1,
    project_id=1,
    message_type="status_update"
)

# スレッドで返信
create_message(
    content="お疲れ様です！バックエンドとの連携確認も済んでいますか？",
    user_id=2,
    parent_id=1,  # 上記メッセージへの返信
    project_id=1
)
```

### 2. ダイレクトメッセージでの相談

```python
# 個人的な相談を送信
create_direct_message(
    content="プルリクエストのレビューをお願いできますか？急ぎではないです。",
    user_id=3,  # 送信者
    recipient_id=2  # 受信者
)

# 返信
create_direct_message(
    content="もちろんです！リンクを送ってください。",
    user_id=2,
    recipient_id=3,
    parent_id=2  # DMのスレッド返信
)
```

### 3. 未読メッセージの確認と既読管理

```python
# 未読メッセージを確認
unread_messages = get_unread_messages(user_id=2)

# 特定のメッセージを既読にする
mark_message_as_read(message_id=5)

# 特定のユーザーとの会話を全て既読にする
mark_conversation_as_read(user_id=2, other_user_id=1)
```

### 4. メッセージの種類別活用

```python
# 質問の投稿
create_message(
    content="このエラーの解決方法がわからないのですが、どなたか知っていますか？",
    user_id=1,
    project_id=1,
    message_type="question"
)

# 回答
create_message(
    content="それは環境変数の設定が原因だと思います。.envファイルを確認してみてください。",
    user_id=2,
    parent_id=3,  # 質問への返信
    message_type="answer"
)

# アナウンス
create_message(
    content="【重要】明日の15:00からシステムメンテナンスを行います。",
    user_id=4,  # PM
    project_id=1,
    message_type="announcement"
)
```

---

## 📋 MCP リソース一覧

- `project://{project_id}` - プロジェクト情報とタスク一覧
- `task://{task_id}` - タスク詳細情報
- `user://{user_id}` - ユーザー情報
- `messages://recent` - 最近のメッセージ一覧

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
│   ├── API.md           # API リファレンス
│   ├── TODO.md          # 開発タスク管理
│   └── fastmcp_guide.md # FastMCP基本ガイド
├── pyproject.toml        # プロジェクト設定・依存関係
├── uv.lock               # 依存関係ロックファイル
└── README.md
```

---

## 🌟 DevLog の特長

### 1. 🔄 シームレスな LLM 統合

Claude や ChatGPT などの LLM から自然言語で操作できます：

- 「プロジェクト X の進捗状況を教えて」
- 「田中さんに完了報告の DM を送って」
- 「未読メッセージをまとめて」

### 2. 📱 Slack 風の使いやすさ

慣れ親しんだ Slack のような操作感で、学習コストを最小限に：

- チャンネル（プロジェクト）での情報共有
- DM での個人的な相談
- スレッドでの文脈を保った議論

### 3. 🔍 コンテキストに応じた情報整理

- プロジェクト・タスク単位での情報管理
- メッセージタイプによる内容の分類
- 既読・未読による情報の優先度付け

### 4. 🚀 開発チームに特化

- タスクと連動したコミュニケーション
- 進捗の自動集約と可視化
- 開発フローに組み込みやすい設計

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

## 🤝 よくある使用シーン

### 朝会での状況共有

```
create_message(
    content="昨日のタスク完了。今日はAPIテストを進めます。",
    user_id=1,
    project_id=1,
    message_type="status_update"
)
```

### 技術的な質問・相談

```
create_message(
    content="TypeScriptの型定義で困っています。アドバイスをいただけませんか？",
    user_id=2,
    project_id=1,
    message_type="question"
)
```

### 急ぎの連絡

```
create_direct_message(
    content="障害対応が必要です。30分後に会議室で打ち合わせできますか？",
    user_id=3,
    recipient_id=1
)
```

### 週次報告のまとめ

LLM に「今週のプロジェクト X の進捗をまとめて」と依頼すれば、自動的にメッセージを分析して報告書を作成。

---

## 📝 ライセンス

MIT License
