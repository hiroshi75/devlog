# DevStatusMCP ツールガイド

**DevStatusMCP** が提供する 16 個のツールの詳細な使用方法とサンプルコードです。

Slack 風の開発状況共有サービスとして、複数人が複数プロジェクトで複数タスクを進める状況を一元管理し、メッセージ形式での進捗管理とコミュニケーションを実現します。

## 📋 目次

- [プロジェクト管理ツール](#プロジェクト管理ツール)
- [タスク管理ツール](#タスク管理ツール)
- [ユーザー管理ツール](#ユーザー管理ツール)
- [メッセージ管理ツール](#メッセージ管理ツール)

---

## 📁 プロジェクト管理ツール

### 1. create_project

新しいプロジェクトを作成します。

**パラメータ：**

- `name` (string, 必須): プロジェクト名
- `description` (string, オプション): プロジェクトの説明

**使用例：**

```json
{
  "name": "create_project",
  "arguments": {
    "name": "新しいWebアプリ",
    "description": "React と Node.js を使用したWebアプリケーション"
  }
}
```

**レスポンス例：**

```json
{
  "id": 1,
  "name": "新しいWebアプリ",
  "description": "React と Node.js を使用したWebアプリケーション",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

### 2. get_projects

すべてのプロジェクトを取得します。

**パラメータ：** なし

**使用例：**

```json
{
  "name": "get_projects",
  "arguments": {}
}
```

**レスポンス例：**

```json
[
  {
    "id": 1,
    "name": "新しいWebアプリ",
    "description": "React と Node.js を使用したWebアプリケーション",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
]
```

### 3. get_project

特定のプロジェクトを取得します。

**パラメータ：**

- `project_id` (integer, 必須): プロジェクト ID

**使用例：**

```json
{
  "name": "get_project",
  "arguments": {
    "project_id": 1
  }
}
```

**レスポンス例：**

```json
{
  "id": 1,
  "name": "新しいWebアプリ",
  "description": "React と Node.js を使用したWebアプリケーション",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

### 4. update_project

プロジェクトを更新します。

**パラメータ：**

- `project_id` (integer, 必須): プロジェクト ID
- `name` (string, オプション): 新しいプロジェクト名
- `description` (string, オプション): 新しい説明

**使用例：**

```json
{
  "name": "update_project",
  "arguments": {
    "project_id": 1,
    "name": "改良されたWebアプリ",
    "description": "React と Node.js を使用したモダンなWebアプリケーション"
  }
}
```

### 5. delete_project

プロジェクトを削除します。

**パラメータ：**

- `project_id` (integer, 必須): プロジェクト ID

**使用例：**

```json
{
  "name": "delete_project",
  "arguments": {
    "project_id": 1
  }
}
```

---

## ✅ タスク管理ツール

### 6. create_task

新しいタスクを作成します。

**パラメータ：**

- `title` (string, 必須): タスクのタイトル
- `project_id` (integer, 必須): 所属するプロジェクト ID
- `description` (string, オプション): タスクの詳細説明
- `status` (string, オプション): タスクの状態（デフォルト: "todo"）
- `assignee_id` (integer, オプション): 担当者のユーザー ID

**ステータス値：**

- `todo`: 未着手
- `in_progress`: 進行中
- `done`: 完了
- `blocked`: ブロック中

**使用例：**

```json
{
  "name": "create_task",
  "arguments": {
    "title": "ユーザー認証機能の実装",
    "project_id": 1,
    "description": "ログイン・ログアウト機能を実装する",
    "status": "todo",
    "assignee_id": 1
  }
}
```

### 7. get_tasks

タスクを取得します（フィルタリング可能）。

**パラメータ（すべてオプション）：**

- `project_id` (integer): プロジェクト ID でフィルタ
- `status` (string): ステータスでフィルタ
- `assignee_id` (integer): 担当者 ID でフィルタ

**使用例：**

```json
{
  "name": "get_tasks",
  "arguments": {
    "project_id": 1,
    "status": "in_progress"
  }
}
```

### 8. get_task

特定のタスクを取得します。

**パラメータ：**

- `task_id` (integer, 必須): タスク ID

**使用例：**

```json
{
  "name": "get_task",
  "arguments": {
    "task_id": 1
  }
}
```

### 9. update_task

タスクを更新します。

**パラメータ：**

- `task_id` (integer, 必須): タスク ID
- `title` (string, オプション): 新しいタイトル
- `description` (string, オプション): 新しい説明
- `status` (string, オプション): 新しいステータス
- `assignee_id` (integer, オプション): 新しい担当者 ID

**使用例：**

```json
{
  "name": "update_task",
  "arguments": {
    "task_id": 1,
    "status": "in_progress"
  }
}
```

### 10. delete_task

タスクを削除します。

**パラメータ：**

- `task_id` (integer, 必須): タスク ID

**使用例：**

```json
{
  "name": "delete_task",
  "arguments": {
    "task_id": 1
  }
}
```

---

## 👤 ユーザー管理ツール

### 11. create_user

新しいユーザーを作成します。

**パラメータ：**

- `username` (string, 必須): ユーザー名
- `email` (string, 必須): メールアドレス

**使用例：**

```json
{
  "name": "create_user",
  "arguments": {
    "username": "tanaka_taro",
    "email": "tanaka@example.com"
  }
}
```

**レスポンス例：**

```json
{
  "id": 1,
  "username": "tanaka_taro",
  "email": "tanaka@example.com",
  "created_at": "2024-01-01T10:00:00"
}
```

### 12. get_users

すべてのユーザーを取得します。

**パラメータ：** なし

**使用例：**

```json
{
  "name": "get_users",
  "arguments": {}
}
```

### 13. get_user

特定のユーザーを取得します。

**パラメータ：**

- `user_id` (integer, 必須): ユーザー ID

**使用例：**

```json
{
  "name": "get_user",
  "arguments": {
    "user_id": 1
  }
}
```

---

## 💬 メッセージ管理ツール

### 14. create_message

新しいメッセージを作成します。

**パラメータ：**

- `content` (string, 必須): メッセージ内容
- `user_id` (integer, 必須): 投稿者のユーザー ID
- `message_type` (string, オプション): メッセージタイプ（デフォルト: "comment"）
- `task_id` (integer, オプション): 関連するタスク ID
- `project_id` (integer, オプション): 関連するプロジェクト ID
- `parent_id` (integer, オプション): 返信先メッセージ ID

**メッセージタイプ：**

- `comment`: 一般的なコメント
- `update`: 進捗更新
- `issue`: 問題報告
- `question`: 質問

**使用例：**

```json
{
  "name": "create_message",
  "arguments": {
    "content": "ユーザー認証機能の実装を開始しました",
    "user_id": 1,
    "message_type": "update",
    "task_id": 1,
    "project_id": 1
  }
}
```

### 15. get_messages

メッセージを取得します（フィルタリング可能）。

**パラメータ（すべてオプション）：**

- `project_id` (integer): プロジェクト ID でフィルタ
- `task_id` (integer): タスク ID でフィルタ
- `user_id` (integer): ユーザー ID でフィルタ
- `message_type` (string): メッセージタイプでフィルタ
- `limit` (integer): 取得件数制限（デフォルト: 100）

**使用例：**

```json
{
  "name": "get_messages",
  "arguments": {
    "project_id": 1,
    "message_type": "update",
    "limit": 20
  }
}
```

### 16. get_message

特定のメッセージを取得します。

**パラメータ：**

- `message_id` (integer, 必須): メッセージ ID

**使用例：**

```json
{
  "name": "get_message",
  "arguments": {
    "message_id": 1
  }
}
```

---

## 🔄 DevStatusMCP の典型的なワークフロー

### プロジェクト開始時

1. `create_project` - プロジェクトを作成
2. `create_user` - チームメンバーを登録
3. `create_task` - 初期タスクを作成

### 日常的な開発作業

1. `get_tasks` - 自分のタスクを確認
2. `update_task` - タスクのステータスを更新
3. `create_message` - 進捗や問題を報告

### プロジェクト管理

1. `get_projects` - プロジェクト一覧を確認
2. `get_messages` - 最新の活動を確認
3. `update_project` - プロジェクト情報を更新

---

## ⚠️ エラーハンドリング

すべてのツールは適切なエラーハンドリングを実装しており、以下のような場合にエラーを返します：

- 存在しない ID を指定した場合
- 必須パラメータが不足している場合
- 無効な値を指定した場合（例：存在しないステータス）

エラーレスポンス例：

```json
{
  "error": "Project not found",
  "details": "Project with ID 999 does not exist"
}
```

---

## 🚀 次のステップ

- [リソースガイド](resources_guide.md) - DevStatusMCP のリソース機能
- [設定ガイド](setup_guide.md) - 各種 MCP クライアントでの設定方法
- [FastMCP ガイド](fastmcp_guide.md) - 開発環境のセットアップ
